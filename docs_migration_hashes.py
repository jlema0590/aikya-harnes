"""Verified predecessor hashes for conservative documentation and SDD upgrades."""
ASSETS = {
    ".claude/rules/01-documentation-policy.md": {
        "sha256": "dd59116a3abc1335b957604e12a0e30d94977df2a5734627f9b5b585d3ce5cba",
        "source": "template/.claude/rules/01-documentation-policy.md",
        "variants": {
            "8681ee81473e693c8901cd82f8180685be83415f22c07954e786b43ccef34c8e": "",
            "dd59116a3abc1335b957604e12a0e30d94977df2a5734627f9b5b585d3ce5cba": ""
        }
    },
    ".claude/skills/documentation-sync/SKILL.md": {
        "sha256": "9a7e89303912a0c1a76bb13f427d622628cba823f787b261b6696b374dd17d01",
        "source": "template/.claude/skills/documentation-sync/SKILL.md",
        "variants": {
            "9a7e89303912a0c1a76bb13f427d622628cba823f787b261b6696b374dd17d01": ""
        }
    },
    ".claude/skills/feature/SKILL.md": {
        "sha256": "a8a57e8c58bf63d375c5ef2e054aa92ec9e4722f950269e08e67f5bd572e3c50",
        "source": "template/.claude/skills/feature/SKILL.md",
        "variants": {
            "a8a57e8c58bf63d375c5ef2e054aa92ec9e4722f950269e08e67f5bd572e3c50": ""
        }
    },
    "CLAUDE.md": {
        "sha256": "f014264239ad0ae8e4ae01ac4110e75c833792cb2994aba6e0f377daf392d37c",
        "source": "template/CLAUDE.md",
        "variants": {
            "22176e2ac0280e71fe994aa7469b11b211f9185d54fe7c31db646edc451bb1df": "\n## Perfil técnico\nLee `.claude/rules/00-project-profile.md` antes de diseñar o modificar la aplicación.\n",
            "ee8ee3c03c48999c53556ef84a37c54e007231adad5faa1d2dbd6b805042451e": "",
            "f7f8dc2c0a5f2047251f5cc3b0d455e5c0c93ae1a8d5376c45d3ddfc030261a0": "\n## Perfil técnico\nLee `.claude/rules/00-project-profile.md` antes de diseñar o modificar la aplicación.\n",
            "b82b0ca7e8663b077d944c1015d3cb31caf918497574029ec6b9f33f3343c330": "\n## Perfil técnico\nLee `.claude/rules/00-project-profile.md` antes de diseñar o modificar la aplicación.\n",
            "f014264239ad0ae8e4ae01ac4110e75c833792cb2994aba6e0f377daf392d37c": ""
        }
    },
    "aikya/scripts/harness/aikya_analyze.py": {
        "sha256": "3b7e1e8856acdc0676bbbddac68d66ed10273ee561dcd70b0542b8dce39ed905",
        "source": "aikya_analyze.py",
        "variants": {
            "4689155ad97bbd76df4896a3a8afb2684a84a31f0971f0786f01aebaccb5ecdc": "",
            "c118a7fb1d9dcf4362fb4400444ca7cf384a435f22715fb9125277fafe357837": "",
            "a55a6687521accf4986394a197df1b851d944533ac57aa2ab81ff258dc078f8a": ""
        }
    },
    "aikya/scripts/harness/aikya_cli.py": {
        "sha256": "f3e397e125d9b23021144863ec9f936bcf12c5ff33f04ed3899f008e51b06611",
        "source": "aikya_cli.py",
        "variants": {
            "12a508b122ba4ff22f64667a1ec7d9314add6e7b8bb8d02409421b33d3fa6eb5": "",
            "2f99c8d9028c7364fab2e520752c6fb54773974d72af5c73ae938d637cfdf8b7": ""
        }
    },
    "aikya/scripts/harness/aikya_requirements.py": {
        "sha256": "10188a3a27554861909012971fbea9c6f6368bd74d935ca484421e9baf20ad27",
        "source": "aikya_requirements.py",
        "variants": {
            "10188a3a27554861909012971fbea9c6f6368bd74d935ca484421e9baf20ad27": ""
        }
    },
    "aikya/scripts/harness/aikya_setup.py": {
        "sha256": "0f126f609618341ee0580c91d7ebc22911bc2389be5afb4973458524640929ac",
        "source": "aikya_setup.py",
        "variants": {
            "1b4dc757d28388b0085b252549f610878de4ec4cc532a6e9a0d4c3196015734a": "",
            "fa337e36815fdc4cc33d3bbd5793ba8acb1424cc7ae71479291251cbbaeffbb4": "",
            "973e326dc84bd1e2f2af64b7be4d8914dcb801440f6f948b63fb4df3a1933c4d": ""
        }
    },
    "aikya/scripts/harness/docs_guard.py": {
        "sha256": "78ba67ba069d0620dc6e86dd629542fb8bfc746cc7c573283a3fa8d379bad596",
        "source": "template/scripts/harness/docs_guard.py",
        "variants": {
            "78ba67ba069d0620dc6e86dd629542fb8bfc746cc7c573283a3fa8d379bad596": ""
        }
    },
    "aikya/scripts/harness/docs_templates_en.py": {
        "sha256": "9e6e36e2c7355a47e2c8da3b8c1d841d93dca17adef42b3e053ffa9d5974bb81",
        "source": "docs_templates_en.py",
        "variants": {
            "9e6e36e2c7355a47e2c8da3b8c1d841d93dca17adef42b3e053ffa9d5974bb81": ""
        }
    },
    "aikya/scripts/harness/docs_templates_es.py": {
        "sha256": "073208a58e8909ff4b183b940609cf538d695959966f46be64e59b8292bef25e",
        "source": "docs_templates_es.py",
        "variants": {
            "073208a58e8909ff4b183b940609cf538d695959966f46be64e59b8292bef25e": ""
        }
    },
    "aikya/scripts/harness/engineering_catalog.py": {
        "sha256": "04af0dedba4edfe63d195e88f2a416180b202fddc6afb0959bde6e6cf77c9421",
        "source": "engineering_catalog.py",
        "variants": {
            "d417c25b60823ed1c964fb98a2ea224da7b48cacb854a5a67eeabdb0c56edf9c": "",
            "04af0dedba4edfe63d195e88f2a416180b202fddc6afb0959bde6e6cf77c9421": ""
        }
    },
    "aikya/scripts/harness/external_skills.py": {
        "sha256": "2700c0e499c1442cceb769a498234952fb82f1bfa0894a5b752f57938c1920fa",
        "source": "template/scripts/harness/external_skills.py",
        "variants": {
            "2700c0e499c1442cceb769a498234952fb82f1bfa0894a5b752f57938c1920fa": ""
        }
    },
    "aikya/scripts/harness/install.py": {
        "sha256": "bd992b4c58e0669fe0d3dc844ffee9e38f6a4e9a27f5870930f4f4a84ef362e2",
        "source": "install.py",
        "variants": {
            "da6fbe4bb8f79f925b6509519f3971b398dc69e2c16cdaf2edf014d234e735f2": "",
            "36fe67ff6e51e02025f26478e2cbfa0094c2a2ca0b98e0eca31745cadeb10c21": "",
            "73890317bd781aa87679537c82d6e7dcd81442bc2e92bff46dbe6c2cd430424e": ""
        }
    },
    "aikya/scripts/harness/skills_registry.py": {
        "sha256": "f61dc0fc6c39da3bf2d455f45dbb4782a0b08ccb79be423b4e973a07fbbcfdbb",
        "source": "template/scripts/harness/skills_registry.py",
        "variants": {
            "410543148a2b22acda9a3c8e61cd20a59c9f5dcae476a32e4188bc272475ec0a": "",
            "8fe7df058538d6d666df2455448bd213417361cf43f25875a871cb31d79ad4e5": "",
            "f61dc0fc6c39da3bf2d455f45dbb4782a0b08ccb79be423b4e973a07fbbcfdbb": ""
        }
    },
    "aikya/scripts/harness/analysis_manifest.py": {
        "source": "analysis_manifest.py",
        "sha256": "262da1ca445886502fb209c586d130ed3498ad97e938a16e33b7e2e3a376f3bd",
        "variants": {
            "262da1ca445886502fb209c586d130ed3498ad97e938a16e33b7e2e3a376f3bd": ""
        }
    },
    "aikya/scripts/harness/doc_bootstrap.py": {
        "source": "doc_bootstrap.py",
        "sha256": "7322cd17df45abca77df0dd95d3e5df6c48f2899a5f76632130644be574a0fe0",
        "variants": {
            "7322cd17df45abca77df0dd95d3e5df6c48f2899a5f76632130644be574a0fe0": "",
            "1704b277530b782e61c6f64f6c8c90ea93fb4cc00862859d2983a0ee41ef9608": "",
            "e7981aa3577522cbeb51bd38eda849547de992ae490ee07fce9141284543fb67": ""
        }
    },
    "aikya/scripts/harness/docs_layout.py": {
        "source": "docs_layout.py",
        "sha256": "06ae2a61f570294cec9f55cd1331c2a7dd4d0576afb6c278cdce9b318c2e5a29",
        "variants": {
            "06ae2a61f570294cec9f55cd1331c2a7dd4d0576afb6c278cdce9b318c2e5a29": "",
            "d42cbfcccf1ee41074abeec710233e97b13020bc3b2ddd0140bea2be8be4055f": ""
        }
    },
    "aikya/scripts/harness/infrastructure.py": {
        "source": "template/scripts/harness/infrastructure.py",
        "sha256": "c26d50ec3369dec6a8589c518c44eae5c246a586b0147d4d12a501d9c2623007",
        "variants": {
            "c26d50ec3369dec6a8589c518c44eae5c246a586b0147d4d12a501d9c2623007": "",
            "f13a5c99a10c1ed48819c9ad22e427828ae0137368f2a65e94fa0d11f2e750a9": "",
            "d992701fb2d3cdeaae14aba323dbc8c005f9db384eaf3ac360bf6e9d9ea32d72": ""
        }
    },
    "aikya/scripts/harness/docs_migration_hashes.py": {
        "source": "docs_migration_hashes.py",
        "sha256": "c25911f9e7b7d343935311bcf7dead2efb9c11204a7d40c2e0acabbdb7651ee5"
    },
    "aikya/scripts/harness/scaffold.py": {
        "source": "template/scripts/harness/scaffold.py",
        "sha256": "47181c3ad2cb22dbec5567953ae51378e115fcba21c9b590405491ffb990f752"
    },
    "aikya/scripts/harness/sdd_assets.py": {
        "source": "sdd_assets.py",
        "sha256": "4cfdb32642540f1049a01eab805c9104b58c2edebf8f45dee5f1777d0be33bdc"
    },
    "aikya/scripts/harness/sdd_engine.py": {
        "source": "sdd_engine.py",
        "sha256": "8aa568768be4d7acafd63ac3639ebbf8e1f1dcb3c310ece838ae70a3c2216da1"
    },
    "aikya/scripts/harness/sdd_localization.py": {
        "source": "sdd_localization.py",
        "sha256": "0e6024f874e0b070f67707f99f3cc299c44c40ba25a534316d9abc68661e0f15"
    }
}
