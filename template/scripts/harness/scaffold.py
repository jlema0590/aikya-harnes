#!/usr/bin/env python3
"""Scaffolding opt-in con generadores oficiales. Python 3.9+ stdlib.

plan nunca ejecuta ni escribe. apply solicita confirmación, no ejecuta shell
ni sobrescribe módulos ya existentes. Para stacks sin CLI fiable hay guía manual.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]


def load_profile(root: Path=ROOT) -> dict:
    path=root/'.harness/project-profile.json'
    profile=json.loads(path.read_text(encoding='utf8'))
    if not isinstance(profile,dict) or not isinstance(profile.get('decisions'),dict):
        raise ValueError('Perfil inválido: instala el harness antes de hacer scaffolding')
    return profile['decisions']


def command_plans(p:dict) -> tuple[list[dict],list[str]]:
    commands=[]
    manual=[]
    pm=p.get('package_manager')
    if pm not in ('npm','pnpm','yarn','bun'):
        pm='npm'
    def add(label,cmd,relative_path,dependency=None):
        commands.append({'label':label,'command':cmd,'creates':relative_path,
                         'requires':dependency or cmd[0]})
    backend=p.get('backend')
    frontend=p.get('frontend')
    mobile=p.get('mobile')
    if backend=='dotnet':
        template='web' if p.get('backend_framework')=='minimal-api' else 'webapi'
        add('Backend ASP.NET Core',['dotnet','new',template,'-o','apps/api'],'apps/api')
    elif backend=='next':
        add('Aplicación Next.js + React',
            ['npx','create-next-app@latest','apps/web','--typescript','--eslint','--app','--yes'],
            'apps/web')
    elif backend=='python':
        manual.append('Python '+p.get('backend_framework','undecided')+
                      ': crear apps/api con el generador oficial del framework y entorno virtual verificado. No se ejecuta pip automáticamente.')
    elif backend=='node' and p.get('backend_framework')=='nestjs':
        add('Backend NestJS',['npx','@nestjs/cli@latest','new','apps/api','--skip-git','--skip-install'],
            'apps/api')
    elif backend=='node':
        manual.append('Node.js '+p.get('backend_framework','undecided')+
                      ': configurar el generador oficial y su versión; no hay comando seguro preseleccionado.')
    elif backend=='java':
        manual.append('Java '+p.get('backend_framework','undecided')+
                      ': utilizar Spring Initializr / code.quarkus.io / Micronaut Launch con versiones verificadas; exportar a apps/api.')
    if frontend=='angular':
        manual.append('Angular: confirmar versión Node y Angular CLI; crear apps/web con ng new una vez aprobada la instalación del CLI.')
    if frontend in ('react','vue') and not (backend=='next' and frontend=='react'):
        folder='apps/frontend' if backend=='next' else 'apps/web'
        template='react-ts' if frontend=='react' else 'vue-ts'
        add('Frontend '+frontend, ['npm','create','vite@latest',folder,'--','--template',template],folder)
    if mobile!='none':
        fw=p.get('mobile_framework')
        if fw=='flutter':
            platforms='android,ios' if mobile=='both' else mobile
            add('Flutter',['flutter','create','--platforms='+platforms,'apps/mobile'],'apps/mobile')
        elif fw=='react-native':
            add('React Native (Expo)',['npx','create-expo-app@latest','apps/mobile'], 'apps/mobile')
            manual.append('Validar si se requiere Expo o React Native bare y configurar SDKs, permisos, variantes y signing.')
        else:
            if mobile in ('android','both'):
                manual.append('Android nativo: generar proyecto Android Studio en apps/android (Kotlin/Java del perfil).')
            if mobile in ('ios','both'):
                manual.append('iOS nativo: generar proyecto Xcode en apps/ios (requiere macOS y Xcode).')
    return commands,manual


def plan(p:dict) -> str:
    cmds,manual=command_plans(p)
    text=['# Engineering Scaffold (generadores oficiales; ejecución opcional)','']
    for item in cmds:
        text.append('- '+item['label']+': '+ ' '.join(item['command']) + '  →  '+item['creates'])
    for note in manual:
        text.append('- MANUAL: '+note)
    if not cmds:
        text.append('- Este stack sólo tiene instrucciones manuales de scaffold.')
    text+=['','Cada comando puede acceder a Internet e instalar dependencias. '
           'Revisa versiones/SDK y los destinos antes de usar `apply`. '
           'Docker/CI/OTel requieren ajustes una vez generada la aplicación.']
    return '\n'.join(text)+'\n'


def apply(p:dict, root:Path, assume_yes:bool=False, runner=subprocess.run) -> int:
    cmds,manual=command_plans(p)
    if p.get('mode')!='new':
        print('No ejecutar scaffold sobre proyecto existente.',file=sys.stderr)
        return 2
    if not cmds:
        print(plan(p))
        return 0 if manual else 1
    # Comprueba TODOS los destinos antes de ejecutar NINGÚN generador.
    for item in cmds:
        dest=(root/item['creates']).resolve()
        if not dest.is_relative_to(root.resolve()):
            print('Ruta fuera del proyecto; abortado.',file=sys.stderr)
            return 2
        if dest.exists():
            print(f'Destino ya existente: {dest}; no se sobrescribe ni ejecuta.',file=sys.stderr)
            return 2
        if not shutil.which(item['requires']):
            print(f'Falta herramienta {item["requires"]}; abortado sin ejecutar.',file=sys.stderr)
            return 2
    # Diagnóstico obligatorio antes de ejecutar generadores; si falta el detector,
    # no se ejecuta código remoto ni se presume que el entorno está preparado.
    import importlib.util
    detector_path=root/'scripts/harness/aikya_requirements.py'
    if not detector_path.exists():
        detector_path=root/'.aikya/runtime/aikya_requirements.py'
    if not detector_path.exists():
        print('Falta el detector de requisitos Aikya. Ejecuta /aikya-init.',file=sys.stderr)
        return 4
    spec=importlib.util.spec_from_file_location('aikya_requirements_local',detector_path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    report=mod.check(p,root)
    if not report['ready']:
        print('Requisitos sin resolver: ejecuta /aikya-doctor. No se ejecutan generadores.',file=sys.stderr)
        for item in report['checks']:
            if item['status']!='ok':
                print(f" - {item['tool']}: {item['status']} (solicitada: {item['expected'] or 'sin especificar'})",file=sys.stderr)
        return 4
    print(plan(p))
    if not assume_yes:
        if input('¿Ejecutar estos generadores (pueden usar Internet y crear archivos)? [s/N]: ').strip().lower() not in ('s','si','sí','y','yes'):
            print('Cancelado.')
            return 0
    (root/'apps').mkdir(exist_ok=True)
    for item in cmds:
        print('EJECUTANDO:',item['command'],flush=True)
        try:
            result=runner(item['command'],cwd=root,check=False,timeout=600)
        except (OSError,subprocess.TimeoutExpired) as exc:
            print('Fallo: '+str(exc),file=sys.stderr)
            return 1
        if result.returncode:
            print('Generador falló. Revisa archivos parciales antes de reintentar.',file=sys.stderr)
            return 1
    if manual:
        print('\nQuedan pasos manuales:\n'+'\n'.join('- '+m for m in manual))
    print('\nGeneradores finalizados. Configura los checks reales de harness.json, integra telemetría y actualiza docs antes de marcar el proyecto listo.')
    return 0


def main(argv=None):
    parser=argparse.ArgumentParser(description='Planificar o ejecutar generadores oficiales de apps')
    parser.add_argument('mode',choices=['plan','apply'])
    parser.add_argument('--yes',action='store_true',help='Confirmación explícita para ejecución desatendida; puede acceder a Internet')
    args=parser.parse_args(argv)
    try:
        p=load_profile(ROOT)
        if args.mode=='plan':
            print(plan(p)); return 0
        return apply(p,ROOT,args.yes)
    except (OSError,ValueError,KeyboardInterrupt,EOFError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr)
        return 2

if __name__=='__main__':
    sys.exit(main())
