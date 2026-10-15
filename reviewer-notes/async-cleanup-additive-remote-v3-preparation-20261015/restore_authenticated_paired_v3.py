"""INERT SOURCE FOR INDEPENDENT REVIEW; SEPARATE AUTHORIZATION BEFORE EXECUTION.

Offline paired byte recovery from actual authenticated additive part readbacks
and the already authenticated base archive checkpoint. Commit and provenance pins
must be independently established outside the inputs; staging is never remote.
No archived source is imported, evaluated, compiled or launched. Nested packaging
bodies remain opaque data. No runtime/dependency/database environment is restored.
Only this reviewed source may later run with python -I -S and explicit pin args.
"""
from pathlib import Path, PurePosixPath
import argparse
import collections
import hashlib
import json
import lzma
import os
import re
import stat

P = Path('/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013')
PARTS = P / 'async-cleanup-full-source-additive-remote-parts'
BASE_ARCHIVE = P / 'async-cleanup-focused-remote-reconstructed.tar.xz'
BASE_PROVENANCE = P / 'async-cleanup-focused-remote-parts/REMOTE_PROVENANCE.json'
BASE_REPORT = P / 'async-cleanup-focused-remote-restore-verification.json'
OUT = P / 'async-cleanup-full-source-additive-remote-paired-restore-v2'
REPOSITORY = 'debgh-workspace/cryptalis-research-lab'
REMOTE_PREFIX = 'recovery/async-cleanup-full-source-additive/parts'
BASE_PREFIX = 'recovery/async-cleanup-focused/parts'
BASE_COMMIT = '86fb0e26ac4032a405b8c077939eb3e288e69db5'
BASE_PROVENANCE_SHA = '93b32a8e71db994724409f506c3040e3aad64c9b03a650cf14df7f970e1d7995'
BASE_REPORT_SHA = 'c83fbc9e129e6d95f2705d82ff3ff55703e3652d705b5bd5b6750107d89d1d92'
A_ARCHIVE = 'CRYPTALIS_ASYNC_CLEANUP_ADDITIVE_RECOVERY_20261015_v2.tar.xz'
B_ARCHIVE = 'CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz'
B_ROOT = 'CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1/'
A_SHA = 'bab72dad661711acc3d8fdf2ab5e84f6abc7eaafd0d1f976023004b08e371262'
B_SHA = '1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af'
A_MANIFEST = 'ADDITIVE_PAYLOAD_MANIFEST-v2.json'
B_MANIFEST = 'FROZEN_PAYLOAD_MANIFEST-v1.json'
A_MANIFEST_SHA = 'b664ead41a5196f410589ef4d8626d3105107e56ac4ac34f8c83603cb71df26a'
B_MANIFEST_SHA = 'e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174'
A_ALLOW_SHA = '5acba866d11b08a8652ac3268db1292e3d89957035b49ce9779e5456e3b71a01'
B_ALLOW_NAME = 'freeze/FREEZE_CONTROL_ALLOWLIST-v1.json'
B_ALLOW_SHA = '8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176'
REVIEW_SHA = '7ce42517888ec76230d8ae4015e97a5d283e3ff047919b0baf0d65b8b5796255'
REVIEW_CLOSURE_SHA = '5206c09b75f1f309dab0614fe826e61550399c659ae6ec38829ca673f3bb552c'
BASE_REVIEW_SHA = 'cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a'
ACCEPTED_RECORDS_SHA = 'e439e3f5f72ce11942624cb888266e3fca5d28f6e368abec780096372f3f5852'
LOGICAL_LIST_SHA = 'd08d157801d02aecee0136ac4e2bbe2136b473e575b00d965b52136a9cc5fd8c'
EMPTY_DIR = 'workspace/cryptalis-executable/evidence/async-cleanup-full-integration-optional38-20261014/candidate-corpus'
MAX_MEMBER = 8 * 1024**2
MAX_STREAM = 64 * 1024**2
MAX_LOGICAL = 96 * 1024**2
DECODER_MEMORY = 128 * 1024**2
FORBIDDEN_LEAVES = {'tests.json', 'rawtests.json', 'readiness.json', 'package-origin.json', 'postgres-start.json', 'postgres-stop.json'}
FORBIDDEN_PARTS = {'.git', '.venv', 'venv', 'env', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'node_modules', 'site-packages', 'runtime', '.ssh', '.aws', '.codex', 'credentials', 'secrets', 'environment', 'dependencies', 'cache', 'toolchain', 'pgdata', 'postgres-data'}

# Generated immutable exact pins are data; no listed live origin is ever opened.
PART_MANIFEST_SHA256 = 'a35df3805ba8a2d0f730acd8c6589d2ddc3ba89b079a439f6af7d3e6492cabfc'
EXPECTED_PARTS = [('part-01.bin',
  96000,
  'cc75b4f388dc59f6a9ba0777af0ac2da6b5eddbb711ec1fb6d5ab2766a5ef9ee',
  'b9962f9157a6368f5a9516ccb786870637b3f12f'),
 ('part-02.bin',
  96000,
  'f930479e2237f9efb6a9120f0709063810c85d164ee7a10f7611d1871aba3d87',
  'f087314a1fce77abe663b80f2c72d682c6a83132'),
 ('part-03.bin',
  96000,
  'baff226a231f607429626b9c2aebcc1f30287595320efa22f7514c973233f459',
  '3e280e40174e8d5f537b2932de968d93d724ece4'),
 ('part-04.bin',
  96000,
  '79d6cd465510b54313997e97bfc71633726016b6cee152198f63454f1d4e6c81',
  '608619f3be412f4582dc8a7f3d7fca46ac99a464'),
 ('part-05.bin',
  96000,
  'd9db2cd83e778b846cce493dca48ad9d088e0bfa46d6ac257ad300cbdf76c833',
  'f1eac00174ee0719337e0f78de521bfd0ee8f4e4'),
 ('part-06.bin',
  96000,
  '6f12132ddf79aa7e2646aee32a0c6ed20ba2b4026ca5ca901f8b48fa69a46c93',
  '3018ccdbeef66552a0974beee68217e289ee0ebb'),
 ('part-07.bin',
  96000,
  '631e912075619f289503fb8666ea1f81409ae3766a26022c00d0e791eda68cd5',
  'e7b1762050eff641da1b51f40cf85b907c736687'),
 ('part-08.bin',
  96000,
  'fe30475d8d6ef323a96e16e5bfa80ea741dc83d452b01cab2564990273b0902e',
  '81e744bdc857cdad951092d65f9175d28ad0ab1e'),
 ('part-09.bin',
  96000,
  '9c717ddf77c995cf72016f1bfc25b1b35fa87d3504d8bfa25514507d362fb480',
  'cce55030e667c1fc7a269607ba57038f101f879b'),
 ('part-10.bin',
  96000,
  'b35c35a5c14ab28deca44309c9ea8be9f3d14994eab2b374d78b378d207f445b',
  '88c391d9782a23fc4c9697ca34580dfbc0382844'),
 ('part-11.bin',
  96000,
  '5c28fb6b63f95d90f663347fdca8b94ae8e8b2e320ccdf2ce5bcf8a5eb09bc2c',
  '231652fdd6b92ad4de146d0b1b1b077ee2aa9c7b'),
 ('part-12.bin',
  96000,
  '3f1454ab915976296b0f287782600b338e5d3bef7a5be15a15b1225698e8fca3',
  '1c753e27ddd3818f457fe88b9a45c1cfdb0c4def'),
 ('part-13.bin',
  96000,
  '5f880fe16a77ff21cc3353b07e3b36c7dffa546d528b1f645a37f27c10bef3d1',
  '0d60c28c656615fe0c5a4d1cba3054e83c642c3d'),
 ('part-14.bin',
  96000,
  'fa85130e7cfabad1e57d3a2a23a5a8e212d0037fd2839f60d7a8d60ce54ce7ee',
  '844d65046f51908ed901c0e933192756a36fd41c'),
 ('part-15.bin',
  96000,
  '722d23879f59c6d7544763f69765f16be27797b48283dcb07b5e571c823e5125',
  'e9269b657bce6c5b22162e5e5b8f8310d6067e2d'),
 ('part-16.bin',
  96000,
  '8f07552b37854a6d364ab4fe93960a4255473f6ecc4c72f331add875f3c58a5f',
  'c0c0079667717d90a8fd3cb6c5715864435bbde2'),
 ('part-17.bin',
  96000,
  '57cc22b48db9c290786814d4573240db6ce106c93ec25ad4fcca395896e39b83',
  'ea19890aab06d97ba6a24f9fd750e74b1f4c257e'),
 ('part-18.bin',
  96000,
  '93285f139f0439b545a2075387af09d11180eef0c3bc4193e392ae4d4d617f70',
  '4381adf36dfa38265a709377e45904abb739b388'),
 ('part-19.bin',
  96000,
  '745bcad5a9b0c071d430b483c95525a2272510d93404316a2bb564afde192588',
  '2142875246b864e785adddc03a9d96323b4c2df8'),
 ('part-20.bin',
  96000,
  'da9c65fda81a90bc0e0cb6c5dc59ba3a89f3d99d150a4d9d16c3b01188e934cd',
  '35fdbeec110b148dffed0beff8f204fbc8d16183'),
 ('part-21.bin',
  96000,
  'c8196bce062fe2583812af0f8042c2ab0e58bf88ff766c8ad19818dc398d6197',
  '16fe944fcb22a982594804c27b7aab30bd5abc41'),
 ('part-22.bin',
  96000,
  '5430b0d2ffbf8e4c76f4f522aa2fe4eb688660da17c621e5d8b63c8dae3d2d0d',
  'e66cffc7f4f0ac052c95c729193e19117d0a6008'),
 ('part-23.bin',
  64040,
  '57e8b16ce762cb539fd8d11d67a535f99759fb6b399113dfffbda926d05650d0',
  '5b1210110e92498a70f56cb9c1e3b6efd6681e2f')]
EXPECTED_REMOTE_FILES = [('MANIFEST.json',
  5784,
  'a35df3805ba8a2d0f730acd8c6589d2ddc3ba89b079a439f6af7d3e6492cabfc',
  '6e4cc1277697195ef0a1f52dc7ca2258fe8d3946'),
 ('part-01.bin',
  96000,
  'cc75b4f388dc59f6a9ba0777af0ac2da6b5eddbb711ec1fb6d5ab2766a5ef9ee',
  'b9962f9157a6368f5a9516ccb786870637b3f12f'),
 ('part-02.bin',
  96000,
  'f930479e2237f9efb6a9120f0709063810c85d164ee7a10f7611d1871aba3d87',
  'f087314a1fce77abe663b80f2c72d682c6a83132'),
 ('part-03.bin',
  96000,
  'baff226a231f607429626b9c2aebcc1f30287595320efa22f7514c973233f459',
  '3e280e40174e8d5f537b2932de968d93d724ece4'),
 ('part-04.bin',
  96000,
  '79d6cd465510b54313997e97bfc71633726016b6cee152198f63454f1d4e6c81',
  '608619f3be412f4582dc8a7f3d7fca46ac99a464'),
 ('part-05.bin',
  96000,
  'd9db2cd83e778b846cce493dca48ad9d088e0bfa46d6ac257ad300cbdf76c833',
  'f1eac00174ee0719337e0f78de521bfd0ee8f4e4'),
 ('part-06.bin',
  96000,
  '6f12132ddf79aa7e2646aee32a0c6ed20ba2b4026ca5ca901f8b48fa69a46c93',
  '3018ccdbeef66552a0974beee68217e289ee0ebb'),
 ('part-07.bin',
  96000,
  '631e912075619f289503fb8666ea1f81409ae3766a26022c00d0e791eda68cd5',
  'e7b1762050eff641da1b51f40cf85b907c736687'),
 ('part-08.bin',
  96000,
  'fe30475d8d6ef323a96e16e5bfa80ea741dc83d452b01cab2564990273b0902e',
  '81e744bdc857cdad951092d65f9175d28ad0ab1e'),
 ('part-09.bin',
  96000,
  '9c717ddf77c995cf72016f1bfc25b1b35fa87d3504d8bfa25514507d362fb480',
  'cce55030e667c1fc7a269607ba57038f101f879b'),
 ('part-10.bin',
  96000,
  'b35c35a5c14ab28deca44309c9ea8be9f3d14994eab2b374d78b378d207f445b',
  '88c391d9782a23fc4c9697ca34580dfbc0382844'),
 ('part-11.bin',
  96000,
  '5c28fb6b63f95d90f663347fdca8b94ae8e8b2e320ccdf2ce5bcf8a5eb09bc2c',
  '231652fdd6b92ad4de146d0b1b1b077ee2aa9c7b'),
 ('part-12.bin',
  96000,
  '3f1454ab915976296b0f287782600b338e5d3bef7a5be15a15b1225698e8fca3',
  '1c753e27ddd3818f457fe88b9a45c1cfdb0c4def'),
 ('part-13.bin',
  96000,
  '5f880fe16a77ff21cc3353b07e3b36c7dffa546d528b1f645a37f27c10bef3d1',
  '0d60c28c656615fe0c5a4d1cba3054e83c642c3d'),
 ('part-14.bin',
  96000,
  'fa85130e7cfabad1e57d3a2a23a5a8e212d0037fd2839f60d7a8d60ce54ce7ee',
  '844d65046f51908ed901c0e933192756a36fd41c'),
 ('part-15.bin',
  96000,
  '722d23879f59c6d7544763f69765f16be27797b48283dcb07b5e571c823e5125',
  'e9269b657bce6c5b22162e5e5b8f8310d6067e2d'),
 ('part-16.bin',
  96000,
  '8f07552b37854a6d364ab4fe93960a4255473f6ecc4c72f331add875f3c58a5f',
  'c0c0079667717d90a8fd3cb6c5715864435bbde2'),
 ('part-17.bin',
  96000,
  '57cc22b48db9c290786814d4573240db6ce106c93ec25ad4fcca395896e39b83',
  'ea19890aab06d97ba6a24f9fd750e74b1f4c257e'),
 ('part-18.bin',
  96000,
  '93285f139f0439b545a2075387af09d11180eef0c3bc4193e392ae4d4d617f70',
  '4381adf36dfa38265a709377e45904abb739b388'),
 ('part-19.bin',
  96000,
  '745bcad5a9b0c071d430b483c95525a2272510d93404316a2bb564afde192588',
  '2142875246b864e785adddc03a9d96323b4c2df8'),
 ('part-20.bin',
  96000,
  'da9c65fda81a90bc0e0cb6c5dc59ba3a89f3d99d150a4d9d16c3b01188e934cd',
  '35fdbeec110b148dffed0beff8f204fbc8d16183'),
 ('part-21.bin',
  96000,
  'c8196bce062fe2583812af0f8042c2ab0e58bf88ff766c8ad19818dc398d6197',
  '16fe944fcb22a982594804c27b7aab30bd5abc41'),
 ('part-22.bin',
  96000,
  '5430b0d2ffbf8e4c76f4f522aa2fe4eb688660da17c621e5d8b63c8dae3d2d0d',
  'e66cffc7f4f0ac052c95c729193e19117d0a6008'),
 ('part-23.bin',
  64040,
  '57e8b16ce762cb539fd8d11d67a535f99759fb6b399113dfffbda926d05650d0',
  '5b1210110e92498a70f56cb9c1e3b6efd6681e2f')]
EXPECTED_PART_MANIFEST = {'archive': 'CRYPTALIS_ASYNC_CLEANUP_ADDITIVE_RECOVERY_20261015_v2.tar.xz',
 'archive_sha256': 'bab72dad661711acc3d8fdf2ab5e84f6abc7eaafd0d1f976023004b08e371262',
 'bytes': 2176040,
 'format': 'async-cleanup-full-source-additive-parts-v1',
 'independent_paired_archive_review_sha256': '7ce42517888ec76230d8ae4015e97a5d283e3ff047919b0baf0d65b8b5796255',
 'independent_paired_review_closure_sha256': '5206c09b75f1f309dab0614fe826e61550399c659ae6ec38829ca673f3bb552c',
 'intended_remote_prefix': 'recovery/async-cleanup-full-source-additive/parts',
 'intended_repository': 'debgh-workspace/cryptalis-research-lab',
 'parts': [{'bytes': 96000,
            'git_blob_sha': 'b9962f9157a6368f5a9516ccb786870637b3f12f',
            'name': 'part-01.bin',
            'sha256': 'cc75b4f388dc59f6a9ba0777af0ac2da6b5eddbb711ec1fb6d5ab2766a5ef9ee'},
           {'bytes': 96000,
            'git_blob_sha': 'f087314a1fce77abe663b80f2c72d682c6a83132',
            'name': 'part-02.bin',
            'sha256': 'f930479e2237f9efb6a9120f0709063810c85d164ee7a10f7611d1871aba3d87'},
           {'bytes': 96000,
            'git_blob_sha': '3e280e40174e8d5f537b2932de968d93d724ece4',
            'name': 'part-03.bin',
            'sha256': 'baff226a231f607429626b9c2aebcc1f30287595320efa22f7514c973233f459'},
           {'bytes': 96000,
            'git_blob_sha': '608619f3be412f4582dc8a7f3d7fca46ac99a464',
            'name': 'part-04.bin',
            'sha256': '79d6cd465510b54313997e97bfc71633726016b6cee152198f63454f1d4e6c81'},
           {'bytes': 96000,
            'git_blob_sha': 'f1eac00174ee0719337e0f78de521bfd0ee8f4e4',
            'name': 'part-05.bin',
            'sha256': 'd9db2cd83e778b846cce493dca48ad9d088e0bfa46d6ac257ad300cbdf76c833'},
           {'bytes': 96000,
            'git_blob_sha': '3018ccdbeef66552a0974beee68217e289ee0ebb',
            'name': 'part-06.bin',
            'sha256': '6f12132ddf79aa7e2646aee32a0c6ed20ba2b4026ca5ca901f8b48fa69a46c93'},
           {'bytes': 96000,
            'git_blob_sha': 'e7b1762050eff641da1b51f40cf85b907c736687',
            'name': 'part-07.bin',
            'sha256': '631e912075619f289503fb8666ea1f81409ae3766a26022c00d0e791eda68cd5'},
           {'bytes': 96000,
            'git_blob_sha': '81e744bdc857cdad951092d65f9175d28ad0ab1e',
            'name': 'part-08.bin',
            'sha256': 'fe30475d8d6ef323a96e16e5bfa80ea741dc83d452b01cab2564990273b0902e'},
           {'bytes': 96000,
            'git_blob_sha': 'cce55030e667c1fc7a269607ba57038f101f879b',
            'name': 'part-09.bin',
            'sha256': '9c717ddf77c995cf72016f1bfc25b1b35fa87d3504d8bfa25514507d362fb480'},
           {'bytes': 96000,
            'git_blob_sha': '88c391d9782a23fc4c9697ca34580dfbc0382844',
            'name': 'part-10.bin',
            'sha256': 'b35c35a5c14ab28deca44309c9ea8be9f3d14994eab2b374d78b378d207f445b'},
           {'bytes': 96000,
            'git_blob_sha': '231652fdd6b92ad4de146d0b1b1b077ee2aa9c7b',
            'name': 'part-11.bin',
            'sha256': '5c28fb6b63f95d90f663347fdca8b94ae8e8b2e320ccdf2ce5bcf8a5eb09bc2c'},
           {'bytes': 96000,
            'git_blob_sha': '1c753e27ddd3818f457fe88b9a45c1cfdb0c4def',
            'name': 'part-12.bin',
            'sha256': '3f1454ab915976296b0f287782600b338e5d3bef7a5be15a15b1225698e8fca3'},
           {'bytes': 96000,
            'git_blob_sha': '0d60c28c656615fe0c5a4d1cba3054e83c642c3d',
            'name': 'part-13.bin',
            'sha256': '5f880fe16a77ff21cc3353b07e3b36c7dffa546d528b1f645a37f27c10bef3d1'},
           {'bytes': 96000,
            'git_blob_sha': '844d65046f51908ed901c0e933192756a36fd41c',
            'name': 'part-14.bin',
            'sha256': 'fa85130e7cfabad1e57d3a2a23a5a8e212d0037fd2839f60d7a8d60ce54ce7ee'},
           {'bytes': 96000,
            'git_blob_sha': 'e9269b657bce6c5b22162e5e5b8f8310d6067e2d',
            'name': 'part-15.bin',
            'sha256': '722d23879f59c6d7544763f69765f16be27797b48283dcb07b5e571c823e5125'},
           {'bytes': 96000,
            'git_blob_sha': 'c0c0079667717d90a8fd3cb6c5715864435bbde2',
            'name': 'part-16.bin',
            'sha256': '8f07552b37854a6d364ab4fe93960a4255473f6ecc4c72f331add875f3c58a5f'},
           {'bytes': 96000,
            'git_blob_sha': 'ea19890aab06d97ba6a24f9fd750e74b1f4c257e',
            'name': 'part-17.bin',
            'sha256': '57cc22b48db9c290786814d4573240db6ce106c93ec25ad4fcca395896e39b83'},
           {'bytes': 96000,
            'git_blob_sha': '4381adf36dfa38265a709377e45904abb739b388',
            'name': 'part-18.bin',
            'sha256': '93285f139f0439b545a2075387af09d11180eef0c3bc4193e392ae4d4d617f70'},
           {'bytes': 96000,
            'git_blob_sha': '2142875246b864e785adddc03a9d96323b4c2df8',
            'name': 'part-19.bin',
            'sha256': '745bcad5a9b0c071d430b483c95525a2272510d93404316a2bb564afde192588'},
           {'bytes': 96000,
            'git_blob_sha': '35fdbeec110b148dffed0beff8f204fbc8d16183',
            'name': 'part-20.bin',
            'sha256': 'da9c65fda81a90bc0e0cb6c5dc59ba3a89f3d99d150a4d9d16c3b01188e934cd'},
           {'bytes': 96000,
            'git_blob_sha': '16fe944fcb22a982594804c27b7aab30bd5abc41',
            'name': 'part-21.bin',
            'sha256': 'c8196bce062fe2583812af0f8042c2ab0e58bf88ff766c8ad19818dc398d6197'},
           {'bytes': 96000,
            'git_blob_sha': 'e66cffc7f4f0ac052c95c729193e19117d0a6008',
            'name': 'part-22.bin',
            'sha256': '5430b0d2ffbf8e4c76f4f522aa2fe4eb688660da17c621e5d8b63c8dae3d2d0d'},
           {'bytes': 64040,
            'git_blob_sha': '5b1210110e92498a70f56cb9c1e3b6efd6681e2f',
            'name': 'part-23.bin',
            'sha256': '57e8b16ce762cb539fd8d11d67a535f99759fb6b399113dfffbda926d05650d0'}],
 'required_base_archive_sha256': '1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af',
 'scope': 'Accepted paired355+516 member and2386 logical-file byte recovery; local parts are staging, never '
          'authenticated remote readbacks.'}
EXPECTED_A_MEMBERS = {'ADDITIVE_PAYLOAD_MANIFEST-v2.json': (153019, 'b664ead41a5196f410589ef4d8626d3105107e56ac4ac34f8c83603cb71df26a'),
 'controls/freeze/FILENAME_ADMISSION.v2.json': (1030189,
                                                'f5f6e258b2024178ce2cb93c2b5058916da4320300f04c2249e514297da2a4e9'),
 'controls/freeze/FREEZE_CONTRACT.v2.json': (33304, 'a0b09f8d271aba41d553d77b0d02e6f8ab7300f32d9a540f07eaa6ba2b17aab3'),
 'controls/freeze/FREEZE_METHOD_INCIDENT.v1.md': (2133,
                                                  'a5da8869ee7bf15d35536d3a45772f2617de4f844c814452970bc927b892dfb5'),
 'controls/freeze/PRE_FREEZE_CHECK.v2.json': (12965,
                                              '525538716c5c0b505c6d78df299b3b45f45e6334edf17243ae8a7b8189cfa2f2'),
 'controls/freeze/RESUMPTION_METADATA.v1.json': (791,
                                                 'cfac7132d06a12b365b4486df04f01d43545c25545816f3da0309e22c791687c'),
 'controls/freeze/freeze-exit.v1.txt': (2, '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'),
 'controls/freeze/freeze-run.v1.log': (827, '7591ff507442c21636e6be8b2b49532557d3c1fa542a3bdc2505453763267450'),
 'controls/freeze/freeze_data_only.v1.py': (34894, '52bbe20f6f0089e26293acb2c86dfa2b8f84c63c5f9bc3e79f3e3fed318c1b18'),
 'controls/freeze/freeze_data_only.v2.py': (35814, 'b8235ed4dfa8a8d88d583768a3c2de8d3f06d45ba4db1bc6192527c59b06e042'),
 'controls/independent/DECISION.json': (872, '6c9b954bf4806e918d12e4ea8b159b7a987a187df6b2b1a951bcbf31d84ec962'),
 'controls/independent/FINAL_CONTINUITY.json': (441,
                                                '6285b6176d477edfab4d687023c16e5b26ac7a0ac8af9f147fb136086adcc0e2'),
 'controls/independent/REVIEW_FILES.sha256': (1790, 'fe2eacbb4c5f2f614ab91f6f8e16b197c5df2e1f16db6334842bf5c8f5db2a17'),
 'controls/independent/accepted-input-hashes.v1.json': (1738065,
                                                        'e439e3f5f72ce11942624cb888266e3fca5d28f6e368abec780096372f3f5852'),
 'controls/independent/filename-admission.v1.json': (1003275,
                                                     'd551485f442be7303743d35c3e48e8f2fbcee62e8e34f0683434eb1e3cd91ec6'),
 'controls/independent/final-continuity-exit.v1.txt': (2,
                                                       '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/independent/final-continuity-run.v1.log': (419,
                                                      'd6bf9e2f1cbf279098a989d0cc9257c9f28560b085d80548354e6b8d07636ae3'),
 'controls/independent/finalize_review.v1.py': (3423,
                                                'ad39f9966c8b562bf2f242ffa43bb6218d46f96b24fb6ebef521f709cae77123'),
 'controls/independent/review-exit.v1.txt': (2, '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/independent/review-link-checks.v1.json': (2995,
                                                     'ce199dbc947b91cfed94e183aa702ba87f1116f98ad8337881790451a479268f'),
 'controls/independent/review-links-exit.v1.txt': (2,
                                                   '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/independent/review-links-run.v1.log': (2995,
                                                  '51bd86d7fe7ac23ec393d5a48fdea43b4dd8992724006e0979dcf0e9ce7e8144'),
 'controls/independent/review-run.v1.log': (278, '11afee7539257a8f5b153eb585561b166eaf6c7f614c3929142b0cded961156f'),
 'controls/independent/review.md': (11447, 'b4410c9e260c18f0681e0f4a11562217ac2c1fa30e92b835ffdfbc889b71015b'),
 'controls/independent/review_data_only.v1.py': (35681,
                                                 '0fe995f14c6024a7b43ff306e698731116422795dc1fb1f837ded609e66c0528'),
 'controls/independent/review_supplement.v1.py': (11051,
                                                  '96649c97ddac546e665f75df3fb4b6ba7ddf6c36acd71c93a30e6b604342e470'),
 'controls/independent/supplement-exit.v1.txt': (2, '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/independent/supplement-run.v1.log': (991,
                                                'ad20f819ca252ec6b6d99af988ff4189ed9c82877b59fe884fef2147cc7a5577'),
 'controls/independent/supplemental-checks.v1.json': (7798,
                                                      '09603ed2d0c7052af8d1c6d28ab02c4583219e6b8f4ff8020d697f1a595a0746'),
 'controls/independent/verification-summary.v1.json': (12906,
                                                       '9e03101085954962ac617c3cc134b458460924bfc071814803f6a1e1d8fd625f'),
 'controls/independent/verify_review_links.v1.py': (3763,
                                                    '30f90938dd575098af951b645ddb6a3f3cf6cea55d938b75d15ef235f716790b'),
 'controls/preparation/BASE_CONTENT_REFERENCES.json': (53161,
                                                       '5d5a0704588908020eda3246f7da57fd48c885f5dfde166a1bb1c69b019d547b'),
 'controls/preparation/EXPLICIT_INPUT_INVENTORY.json': (2384157,
                                                        'fd2137cf020aa599d3a6d92891599632b1ec237f76c06b0b2d60d5550713ecac'),
 'controls/preparation/INPUT_ADMISSION.initial.json': (1654479,
                                                       '50816e159c2b0c6428efd0e62456d7ead7a25739202404b034ce5521ee51b37c'),
 'controls/preparation/INPUT_ADMISSION.json': (1654479,
                                               '50816e159c2b0c6428efd0e62456d7ead7a25739202404b034ce5521ee51b37c'),
 'controls/preparation/METADATA_CLOSURE_QA.json': (3677,
                                                   '3b352a9d64f939bae34c76b8fac1c3f110b9d32dcd8d7625270db1cac5a8122f'),
 'controls/preparation/METHOD_INCIDENTS.md': (2480, 'c427c8c3cbb9532ea27476f7528226ff9c877c9d7b3ed50e4e4bd86c3aaaa5a0'),
 'controls/preparation/NEW_CONTENT_OBJECTS.json': (181521,
                                                   '1969514813e0ac05e9a43c9a784835e25dbcc26363c750e69586d1e24443b29e'),
 'controls/preparation/PREPARATION_CONTROL_INVENTORY.json': (4012,
                                                             '34bc345c7f263925d72b1669ad7b8a615c01af0908a5e6c44ec7d531ee4fbb5e'),
 'controls/preparation/PREPARATION_FILES.sha256': (2558,
                                                   '890ca1ec048581410818d0a5fee0dcfe6a3f41ef95fd99968c939925f2832d4d'),
 'controls/preparation/PREPARATION_REVIEW.md': (10092,
                                                'd04434d4585a33076b738a6b906fe9e6d9ec82ea2d70e846f7d0555e04434f2d'),
 'controls/preparation/PREPARATION_SUMMARY.json': (9567,
                                                   '32d0ab0e82579680cc69b31ecb343c7629a219f008c5e029994eb30f5ab7a7f1'),
 'controls/preparation/PROPOSED_FREEZE_RESTORE.md': (7843,
                                                     'e74d3ef255301770402f4a94b276b58177cd2b388d1938f04e18521ff426c35d'),
 'controls/preparation/PROPOSED_RESTORE_MAP.json': (1115477,
                                                    '47d885a2ed5c3d36e475a02b4a7aa9d64fbf6ab174b3035a02ef037112bc9873'),
 'controls/preparation/RECORD_CONSISTENCY_QA.json': (2535,
                                                     'ee576b272bbc3a878709d33ca0cb7d047b6d2e25a34a091793c93b0bca5d6722'),
 'controls/preparation/check_metadata_closure.py': (2651,
                                                    'cd9a24581737aaa7d98a17ba1351042d6d7aa7849cf9ae3860482c324964950f'),
 'controls/preparation/inventory-exit-v1.txt': (2, '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'),
 'controls/preparation/inventory-exit-v2.txt': (2, '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/preparation/inventory-run-v1.log': (876, 'c37c2eec914f7457874328c38a16f0d649632a67f08d1df212210b47f3d41361'),
 'controls/preparation/inventory-run-v2.log': (803, '013cd8d9839b9c558d491a55f4400a00de1ab8a75a70680a9b4bb49dd64eb257'),
 'controls/preparation/inventory_data_only.initial.py': (33562,
                                                         '6f830045389738b417daedf711cbaa4366d5edd17e64cfeeb8dd9240967501d5'),
 'controls/preparation/inventory_data_only.py': (33850,
                                                 'a2ca3e3fd0f43db57ca9b06c8ff69fed57dd6d00d73346c1f1107f4ba30f2d70'),
 'controls/preparation/metadata-closure-exit.txt': (2,
                                                    '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/preparation/metadata-closure-run.log': (3677,
                                                   '881d867263e457b5c27fddf1f5c82088bbb0f31056197d22a540d6dd6fedb477'),
 'controls/preparation/record-qa-exit.initial.txt': (2,
                                                     '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'),
 'controls/preparation/record-qa-exit.txt': (2, '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'controls/preparation/record-qa-run.initial.log': (304,
                                                    '6648ba37f91d745436c07d1617b449003af3b5c60bfd2ed5f8108905e682c2c8'),
 'controls/preparation/record-qa-run.log': (2535, '274c088c345cdfdb794ed32d291f00f2de493616c6ff850c835c16390936a20b'),
 'controls/preparation/validate_inventory_data.initial.py': (5398,
                                                             '83087e47b9d60067d349410fcba44d7b8d189ad80e80d4397a7fa6e9df7d7d3a'),
 'controls/preparation/validate_inventory_data.py': (5420,
                                                     '8171d8b5090493d35996d18378cac75f9fcaf4f72d217454b25f9c4f74c96237'),
 'objects/sha256/008b7e99061090da0fb81bd71cebc47661f364a4aeb734257d4dc75098bd89cf': (2779,
                                                                                     '008b7e99061090da0fb81bd71cebc47661f364a4aeb734257d4dc75098bd89cf'),
 'objects/sha256/009b35457b4fa065477cf03e5296c24e3b0ce3520ae2ade0d1683b8e3b97c7ca': (3071,
                                                                                     '009b35457b4fa065477cf03e5296c24e3b0ce3520ae2ade0d1683b8e3b97c7ca'),
 'objects/sha256/0103b397775ce82e7040ac86fb776ab276868694018556de4afc68edb4aae936': (25097,
                                                                                     '0103b397775ce82e7040ac86fb776ab276868694018556de4afc68edb4aae936'),
 'objects/sha256/027b3f300e93416ed22f0175e3c4ce0a7782627dcdea02acb6b5f83d695094ea': (921,
                                                                                     '027b3f300e93416ed22f0175e3c4ce0a7782627dcdea02acb6b5f83d695094ea'),
 'objects/sha256/02b0b3616bdf817c152b16a415746ad8ecf9b804d05505e90ed088e4c852f85e': (3177,
                                                                                     '02b0b3616bdf817c152b16a415746ad8ecf9b804d05505e90ed088e4c852f85e'),
 'objects/sha256/0357bf43169efb81aaa8de5d8c03a005d949b9a7eb18cfde8894e87259e855ed': (870,
                                                                                     '0357bf43169efb81aaa8de5d8c03a005d949b9a7eb18cfde8894e87259e855ed'),
 'objects/sha256/06a18d5cfe9f0d3657405bf01177405554a7eee70abab99068bf305ac7869a31': (5944,
                                                                                     '06a18d5cfe9f0d3657405bf01177405554a7eee70abab99068bf305ac7869a31'),
 'objects/sha256/06a82a65a0ce3185dfabf55533371849cd9d5cdf1fbbe021fb6ba53808fcb428': (24967,
                                                                                     '06a82a65a0ce3185dfabf55533371849cd9d5cdf1fbbe021fb6ba53808fcb428'),
 'objects/sha256/06faee4db0bd3b2ce9facaa56800895a7bd171f4d6328ecc7f44c14e4b4212da': (380,
                                                                                     '06faee4db0bd3b2ce9facaa56800895a7bd171f4d6328ecc7f44c14e4b4212da'),
 'objects/sha256/079698e7f98f63f8c587d0eeb99740d515bec9f7d30631e044502557e9102b9d': (2482090,
                                                                                     '079698e7f98f63f8c587d0eeb99740d515bec9f7d30631e044502557e9102b9d'),
 'objects/sha256/09491ae3e4d95a881ab889a555debdba0ab903ef6c18980cc5417f9e0b1c155b': (9322,
                                                                                     '09491ae3e4d95a881ab889a555debdba0ab903ef6c18980cc5417f9e0b1c155b'),
 'objects/sha256/0b20eb9e8270ccef3f5cd9d1ddb547deb8b71127a8157385ebc845528e99c888': (4157,
                                                                                     '0b20eb9e8270ccef3f5cd9d1ddb547deb8b71127a8157385ebc845528e99c888'),
 'objects/sha256/0c395dc7345521dc0c9e5493964741fcfdb137dfcd3f4a96825c33eacbd72f65': (27514,
                                                                                     '0c395dc7345521dc0c9e5493964741fcfdb137dfcd3f4a96825c33eacbd72f65'),
 'objects/sha256/0c9042349d27b6af8d7ebc6421fdbcdf9473588a63b3d1c262429088f9ba284e': (13595,
                                                                                     '0c9042349d27b6af8d7ebc6421fdbcdf9473588a63b3d1c262429088f9ba284e'),
 'objects/sha256/0cd5eb42be8cb1943e5844b77c016babf92eabafe490a362b369500d43692043': (3967,
                                                                                     '0cd5eb42be8cb1943e5844b77c016babf92eabafe490a362b369500d43692043'),
 'objects/sha256/0d2f033079b522e0b0017d25e4bd62d8fdf832c238a7f8184f788c215cb2875c': (491,
                                                                                     '0d2f033079b522e0b0017d25e4bd62d8fdf832c238a7f8184f788c215cb2875c'),
 'objects/sha256/127239a40e424259524ac8cba00f6ff454fe64f5a772c30bb43dcd6e05c875f1': (2620,
                                                                                     '127239a40e424259524ac8cba00f6ff454fe64f5a772c30bb43dcd6e05c875f1'),
 'objects/sha256/1283fd8cacf696d74eb19955fab503a446810bcb01a7ca931c2efc285513feac': (5361,
                                                                                     '1283fd8cacf696d74eb19955fab503a446810bcb01a7ca931c2efc285513feac'),
 'objects/sha256/138e30d9b3951cc71a45c0c055873e517315a137b3828f1f26d2d6b0f91bfa20': (4946,
                                                                                     '138e30d9b3951cc71a45c0c055873e517315a137b3828f1f26d2d6b0f91bfa20'),
 'objects/sha256/14beadac928b56caa8397e27145f51ab3d6f3b91071be51aeef5b5f8297aea3c': (2453,
                                                                                     '14beadac928b56caa8397e27145f51ab3d6f3b91071be51aeef5b5f8297aea3c'),
 'objects/sha256/15c3fb136a1433d3e587792cfa5955be6699773c335ee7ea8b801fdb63704faf': (917,
                                                                                     '15c3fb136a1433d3e587792cfa5955be6699773c335ee7ea8b801fdb63704faf'),
 'objects/sha256/15e6aeb1ca77b147be01f0baebc5abbc9ad96128387af1872b066f4bedd8919f': (620,
                                                                                     '15e6aeb1ca77b147be01f0baebc5abbc9ad96128387af1872b066f4bedd8919f'),
 'objects/sha256/15f952c7136c1b55e60af68feec89fdefd4ed13c6286053aff68abf107515306': (415311,
                                                                                     '15f952c7136c1b55e60af68feec89fdefd4ed13c6286053aff68abf107515306'),
 'objects/sha256/1875b359fda72e1c79625b9ce3f1de78fd9dbea6ce975f82a8e16c2e1ec6fe20': (217,
                                                                                     '1875b359fda72e1c79625b9ce3f1de78fd9dbea6ce975f82a8e16c2e1ec6fe20'),
 'objects/sha256/18b6a74a6f02d8b2dc737ae983cd37ab7d6e2fcaaba9d40f2ad121a2ba919a50': (1473,
                                                                                     '18b6a74a6f02d8b2dc737ae983cd37ab7d6e2fcaaba9d40f2ad121a2ba919a50'),
 'objects/sha256/19668392369b641ab381440875a8e25d0f9349f17140ca8675c3b6c20bd46783': (1212,
                                                                                     '19668392369b641ab381440875a8e25d0f9349f17140ca8675c3b6c20bd46783'),
 'objects/sha256/1abe2c52a9fc32f8102339fea0735d773a0ba55f0cbd456a078bfa473e4240d9': (955,
                                                                                     '1abe2c52a9fc32f8102339fea0735d773a0ba55f0cbd456a078bfa473e4240d9'),
 'objects/sha256/1b9d377f81177b7e7d2539519b2f0c854ee90f7d88088b7a40d509503baaa1a1': (524,
                                                                                     '1b9d377f81177b7e7d2539519b2f0c854ee90f7d88088b7a40d509503baaa1a1'),
 'objects/sha256/1bb6715858065d3262ceca5624b30e145c75f69bb9808e05f62d9bf68b6f4e42': (25309,
                                                                                     '1bb6715858065d3262ceca5624b30e145c75f69bb9808e05f62d9bf68b6f4e42'),
 'objects/sha256/1ca6e0ef22a6d157ccbd0eba13f2e85ec5b6f77eb861e611abb8f4e3b06b8a24': (57,
                                                                                     '1ca6e0ef22a6d157ccbd0eba13f2e85ec5b6f77eb861e611abb8f4e3b06b8a24'),
 'objects/sha256/1cee4b9553957c90d6f1b0e1f7cff3070674f503efddf3336ccedd5da51680c4': (972,
                                                                                     '1cee4b9553957c90d6f1b0e1f7cff3070674f503efddf3336ccedd5da51680c4'),
 'objects/sha256/1dd84e5d6f90a8cbf35603d306835d3d801d05d121ea206f4c5e448a213654e8': (319,
                                                                                     '1dd84e5d6f90a8cbf35603d306835d3d801d05d121ea206f4c5e448a213654e8'),
 'objects/sha256/1f7f9acbbc2677d9537dfa5bba83bf2ec4defb34e2e828b5629d9b384c913b38': (10560,
                                                                                     '1f7f9acbbc2677d9537dfa5bba83bf2ec4defb34e2e828b5629d9b384c913b38'),
 'objects/sha256/22dbc3d59208d8bc6cbd8806a73e8c7258a12af623d9731a7ddaa1fc73fd172c': (19122,
                                                                                     '22dbc3d59208d8bc6cbd8806a73e8c7258a12af623d9731a7ddaa1fc73fd172c'),
 'objects/sha256/25529e24e5190895f76a19a94520cc15ad03d82ef3f7cc423a3c57226655d49e': (35651,
                                                                                     '25529e24e5190895f76a19a94520cc15ad03d82ef3f7cc423a3c57226655d49e'),
 'objects/sha256/2561de0a8d6acf1e1c6e6afe1970f0add320b6461fee184241eb78392f3c87cd': (496,
                                                                                     '2561de0a8d6acf1e1c6e6afe1970f0add320b6461fee184241eb78392f3c87cd'),
 'objects/sha256/26b44d9f16043886c5492ec902c71b52b46634b567b98e156cd8b59e338ce8f6': (4946,
                                                                                     '26b44d9f16043886c5492ec902c71b52b46634b567b98e156cd8b59e338ce8f6'),
 'objects/sha256/26facc7a43318893e8a425b887cd0ad00d5302d1ee1dfe5f0361c25e036c837a': (33057,
                                                                                     '26facc7a43318893e8a425b887cd0ad00d5302d1ee1dfe5f0361c25e036c837a'),
 'objects/sha256/275f4e0bbe4b9ce74e5b285393a499c5496f5af9edc9cb77c330fa630d137144': (9673,
                                                                                     '275f4e0bbe4b9ce74e5b285393a499c5496f5af9edc9cb77c330fa630d137144'),
 'objects/sha256/2a18fa0a3b2e78c75a46809b619f9f8bca3449dbba77c2a7257c8e135bae8904': (3575,
                                                                                     '2a18fa0a3b2e78c75a46809b619f9f8bca3449dbba77c2a7257c8e135bae8904'),
 'objects/sha256/2a39fe6a39bee0d96fbb6fc0b1ce4048e26025b42301b29eee2152f9cdac3b97': (98902,
                                                                                     '2a39fe6a39bee0d96fbb6fc0b1ce4048e26025b42301b29eee2152f9cdac3b97'),
 'objects/sha256/2a5a9bbdf0dd3e2a8b6fc38f8eca1cde95374bde811d138e15f16f1c72fe7917': (74569,
                                                                                     '2a5a9bbdf0dd3e2a8b6fc38f8eca1cde95374bde811d138e15f16f1c72fe7917'),
 'objects/sha256/2c44541185251ee78b02dba2f0fd1c34b7ef6acfaa1e334b92b041804a80c269': (83101,
                                                                                     '2c44541185251ee78b02dba2f0fd1c34b7ef6acfaa1e334b92b041804a80c269'),
 'objects/sha256/2c91256cf116487e213880391886552e30c8fab2511bdffe42d394b6a847b132': (86710,
                                                                                     '2c91256cf116487e213880391886552e30c8fab2511bdffe42d394b6a847b132'),
 'objects/sha256/302db3179b1cee7db69115dd54d0dd28c3cb95034c92d51c6e57541b23c8bccf': (569,
                                                                                     '302db3179b1cee7db69115dd54d0dd28c3cb95034c92d51c6e57541b23c8bccf'),
 'objects/sha256/305417b452f4274e2f6930f88142b75c649d8ddcc4a03495e351245b720e5957': (497,
                                                                                     '305417b452f4274e2f6930f88142b75c649d8ddcc4a03495e351245b720e5957'),
 'objects/sha256/30d17fe1a69fd3fd33e78a55f0c545a12742794da4e81248582f9e0502a00442': (693,
                                                                                     '30d17fe1a69fd3fd33e78a55f0c545a12742794da4e81248582f9e0502a00442'),
 'objects/sha256/33280f8b0c03284642deab63a00ac30f003b9463b3be4de0b102e580aa886f2f': (25109,
                                                                                     '33280f8b0c03284642deab63a00ac30f003b9463b3be4de0b102e580aa886f2f'),
 'objects/sha256/364cc86b516350696247937154e7e40f0490ffdc1064f53879165abd2ebb67cc': (419227,
                                                                                     '364cc86b516350696247937154e7e40f0490ffdc1064f53879165abd2ebb67cc'),
 'objects/sha256/37439866c0486ff8ee2c1a90f65d7759e72f100117bc9326f313af631befcd59': (2234,
                                                                                     '37439866c0486ff8ee2c1a90f65d7759e72f100117bc9326f313af631befcd59'),
 'objects/sha256/37ed3b6680eb74b75041cbe8209680306b8adb07e641ce80d436f39d2b20e5bf': (83147,
                                                                                     '37ed3b6680eb74b75041cbe8209680306b8adb07e641ce80d436f39d2b20e5bf'),
 'objects/sha256/388a3ea6ea74cf5d54e19d04845e65d6a12d8553bf1b20e60a1e4dffad1f0138': (83228,
                                                                                     '388a3ea6ea74cf5d54e19d04845e65d6a12d8553bf1b20e60a1e4dffad1f0138'),
 'objects/sha256/3c40bf547baa8bd25e537c022c3662bce02813b61e4d6684484fbbdee754ead0': (1284,
                                                                                     '3c40bf547baa8bd25e537c022c3662bce02813b61e4d6684484fbbdee754ead0'),
 'objects/sha256/3d26706d56b6cf6634113fc2eeafa161f87c3095c5b55f6b25471fc6f266f4fe': (2998,
                                                                                     '3d26706d56b6cf6634113fc2eeafa161f87c3095c5b55f6b25471fc6f266f4fe'),
 'objects/sha256/3d796a7e3d55e4f3d4735b29d26b0e0d379aea2efd6c2dbb00138ed4b8318caf': (647,
                                                                                     '3d796a7e3d55e4f3d4735b29d26b0e0d379aea2efd6c2dbb00138ed4b8318caf'),
 'objects/sha256/3db0ed2548632ecc11452863578514b6a45f04887eb4692c124363686d6cd8d8': (11390,
                                                                                     '3db0ed2548632ecc11452863578514b6a45f04887eb4692c124363686d6cd8d8'),
 'objects/sha256/3df95b9d798341d9de73226b59500428fb7dcef2cbf887b306f0419d362f095e': (8577,
                                                                                     '3df95b9d798341d9de73226b59500428fb7dcef2cbf887b306f0419d362f095e'),
 'objects/sha256/3e23121e83751e73333a7e1488450d604f97bc0c66c61748a45efe89dfdf2963': (1252,
                                                                                     '3e23121e83751e73333a7e1488450d604f97bc0c66c61748a45efe89dfdf2963'),
 'objects/sha256/3e632059c35213f17b600dfc0c65f77b49adeddcb1664afd965123995bc02c53': (30525,
                                                                                     '3e632059c35213f17b600dfc0c65f77b49adeddcb1664afd965123995bc02c53'),
 'objects/sha256/3f01696d731036b20d1ed814a90cb3f5395bfe4e3115c98bf1b5131ddd9add13': (217,
                                                                                     '3f01696d731036b20d1ed814a90cb3f5395bfe4e3115c98bf1b5131ddd9add13'),
 'objects/sha256/3fd95c533875141d9f8178694e95fa52f61f0e478e6389d08b21f59b9e87137a': (8533,
                                                                                     '3fd95c533875141d9f8178694e95fa52f61f0e478e6389d08b21f59b9e87137a'),
 'objects/sha256/41972f42313c765c0a7c927ac8c068ba88559889c744edcbc41be76b65af980d': (10974,
                                                                                     '41972f42313c765c0a7c927ac8c068ba88559889c744edcbc41be76b65af980d'),
 'objects/sha256/42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c': (138881,
                                                                                     '42150bab589fcb80083dafb8bd34186c5040776950fa1f5b04b11a43c1e3b36c'),
 'objects/sha256/421b346474655edd47a35293fbefc99c5f5bd005682d8502b975006e717282d1': (18303,
                                                                                     '421b346474655edd47a35293fbefc99c5f5bd005682d8502b975006e717282d1'),
 'objects/sha256/42fc29a61c4a260df5d618dead78d74b187dcdca5bc23e233b7587d7080bd3f8': (689,
                                                                                     '42fc29a61c4a260df5d618dead78d74b187dcdca5bc23e233b7587d7080bd3f8'),
 'objects/sha256/434aff8c7e226e8ea5f8be3a5abc3a258c46bb58a3367e9b1d20d835a01167da': (3815,
                                                                                     '434aff8c7e226e8ea5f8be3a5abc3a258c46bb58a3367e9b1d20d835a01167da'),
 'objects/sha256/43b74144bcf81d793fbfea0dc9ba88b4b819a1609d0e69f7bb9eb2bb466f7d8d': (317,
                                                                                     '43b74144bcf81d793fbfea0dc9ba88b4b819a1609d0e69f7bb9eb2bb466f7d8d'),
 'objects/sha256/4413ccdfd9148f7b0cc4513279453a1bb37ca34ecb25bcb84ce869ce21a18c08': (423,
                                                                                     '4413ccdfd9148f7b0cc4513279453a1bb37ca34ecb25bcb84ce869ce21a18c08'),
 'objects/sha256/45ac59321a38587cf7958c19571a06a4acb90825b8fb3e2e474ca8b6fd777275': (3247,
                                                                                     '45ac59321a38587cf7958c19571a06a4acb90825b8fb3e2e474ca8b6fd777275'),
 'objects/sha256/4650dcc1c3c5e0e48a233e70324de8771a26ad5f99197f615fe416905b6b3fd0': (314939,
                                                                                     '4650dcc1c3c5e0e48a233e70324de8771a26ad5f99197f615fe416905b6b3fd0'),
 'objects/sha256/46773c0bfbf8218fdf8c12f4e3615f216bfba31802df74714a754d96995150f7': (3772,
                                                                                     '46773c0bfbf8218fdf8c12f4e3615f216bfba31802df74714a754d96995150f7'),
 'objects/sha256/4800ce1a8e21685d063daf84882e36885759b2b30bcd3c3ad43c6a688b2299ba': (149364,
                                                                                     '4800ce1a8e21685d063daf84882e36885759b2b30bcd3c3ad43c6a688b2299ba'),
 'objects/sha256/4924dc4fdd39b3136eee92b0ff9f3fdcc929ae51f8203298647f8a5078e9a2a9': (8856,
                                                                                     '4924dc4fdd39b3136eee92b0ff9f3fdcc929ae51f8203298647f8a5078e9a2a9'),
 'objects/sha256/4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f': (4154,
                                                                                     '4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f'),
 'objects/sha256/4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8': (15,
                                                                                     '4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8'),
 'objects/sha256/4de2c2459ce1102d764008c0ee1957eb9be3a99200ee9723b9933c8f7ee302a2': (187,
                                                                                     '4de2c2459ce1102d764008c0ee1957eb9be3a99200ee9723b9933c8f7ee302a2'),
 'objects/sha256/501d24cd27866cbc1bc9440e32c395a1eba954c4e1a24da75b6a949cb9c64e2e': (2843,
                                                                                     '501d24cd27866cbc1bc9440e32c395a1eba954c4e1a24da75b6a949cb9c64e2e'),
 'objects/sha256/507780102d78f43868f43222c29850783e7b593eb535e4325cc95740ae2b3e7d': (10361,
                                                                                     '507780102d78f43868f43222c29850783e7b593eb535e4325cc95740ae2b3e7d'),
 'objects/sha256/519514b9d4da1b4266255267bc96accf02d977cf2feff7872b0468b8f02f0861': (299,
                                                                                     '519514b9d4da1b4266255267bc96accf02d977cf2feff7872b0468b8f02f0861'),
 'objects/sha256/51fb8e9bd258f6f16bfa467e2725ae3edccd54bd273f131b52626f6da5552e28': (651,
                                                                                     '51fb8e9bd258f6f16bfa467e2725ae3edccd54bd273f131b52626f6da5552e28'),
 'objects/sha256/521f58ea2cf6c66b3490e58613a80d76580056fbc330c2c896bc0f8a97d85ead': (32689,
                                                                                     '521f58ea2cf6c66b3490e58613a80d76580056fbc330c2c896bc0f8a97d85ead'),
 'objects/sha256/522ce25b5a88df2159d4ea4a0f60f31ed4d041f0a528d33238ec4c476f7abe60': (713,
                                                                                     '522ce25b5a88df2159d4ea4a0f60f31ed4d041f0a528d33238ec4c476f7abe60'),
 'objects/sha256/5294736cb2d5297b6531e867cd0d6480e1eb10ec400629476b3b4da82d6a89ea': (1481,
                                                                                     '5294736cb2d5297b6531e867cd0d6480e1eb10ec400629476b3b4da82d6a89ea'),
 'objects/sha256/52d918b73490a76a2f2ccd4fbdbb4625cda4be293cfae46fdd2b790b1c4c434f': (381,
                                                                                     '52d918b73490a76a2f2ccd4fbdbb4625cda4be293cfae46fdd2b790b1c4c434f'),
 'objects/sha256/5415185e32c8e3ee581c87d8d91b3b06f7394d027f8e05a5d462afa3b1066694': (26852,
                                                                                     '5415185e32c8e3ee581c87d8d91b3b06f7394d027f8e05a5d462afa3b1066694'),
 'objects/sha256/554b953548454181ebf5722a5badc264390ca3cd9855047f51fe82a194177818': (25179,
                                                                                     '554b953548454181ebf5722a5badc264390ca3cd9855047f51fe82a194177818'),
 'objects/sha256/55b4d01b456876cd92c9124b0c0d92fe51e68d1c15356a82834ad524837c92fe': (84677,
                                                                                     '55b4d01b456876cd92c9124b0c0d92fe51e68d1c15356a82834ad524837c92fe'),
 'objects/sha256/55e937ee7d5fe2b76a62af3bb8bdcb5ab076c70f631441ca414e49232afd890f': (33595,
                                                                                     '55e937ee7d5fe2b76a62af3bb8bdcb5ab076c70f631441ca414e49232afd890f'),
 'objects/sha256/55eda984fff9d31b4a8a07b1e8bb9858a0c7ff7c87138884f125903392a90d6e': (2316,
                                                                                     '55eda984fff9d31b4a8a07b1e8bb9858a0c7ff7c87138884f125903392a90d6e'),
 'objects/sha256/55f3ca6716677dd145c63f67a47ba745cd0241f4d41f82f07e447118cb942e1d': (113667,
                                                                                     '55f3ca6716677dd145c63f67a47ba745cd0241f4d41f82f07e447118cb942e1d'),
 'objects/sha256/561b8abebcead2ced4aa02eb870950514bf96fd8aca85613e97e6afc9fc9607e': (6325,
                                                                                     '561b8abebcead2ced4aa02eb870950514bf96fd8aca85613e97e6afc9fc9607e'),
 'objects/sha256/565e784ba40ac9afa23b6b725d3696575e632ac5a88154b2a21cb4dd9e9655a7': (23,
                                                                                     '565e784ba40ac9afa23b6b725d3696575e632ac5a88154b2a21cb4dd9e9655a7'),
 'objects/sha256/57d06624b0391b2d45d8916070eb46ea208a0f8c905c26849e1a0b4e0ae4a552': (1780,
                                                                                     '57d06624b0391b2d45d8916070eb46ea208a0f8c905c26849e1a0b4e0ae4a552'),
 'objects/sha256/58edeb48065f17e98a3c5eea62fd53eae8e960a054cb3b65d7e80294d1b75ba2': (430800,
                                                                                     '58edeb48065f17e98a3c5eea62fd53eae8e960a054cb3b65d7e80294d1b75ba2'),
 'objects/sha256/5946be8dab54bd68669af2f8e5bf0ca335fcec74024f1321c343e87e0938eafa': (2704,
                                                                                     '5946be8dab54bd68669af2f8e5bf0ca335fcec74024f1321c343e87e0938eafa'),
 'objects/sha256/5a496a6cab1ad7937144f660f2eb33af45724588cb2c39922c4b772027461bc5': (145,
                                                                                     '5a496a6cab1ad7937144f660f2eb33af45724588cb2c39922c4b772027461bc5'),
 'objects/sha256/5a682553a768b9d2a85b431123b76fc0e3e7ffd7a9a0776d6a049278b73b7803': (33860,
                                                                                     '5a682553a768b9d2a85b431123b76fc0e3e7ffd7a9a0776d6a049278b73b7803'),
 'objects/sha256/5aa372f3e7b8913228fffd0c983644edf9d79029059e080717d04b5deeada355': (1638,
                                                                                     '5aa372f3e7b8913228fffd0c983644edf9d79029059e080717d04b5deeada355'),
 'objects/sha256/5af253bd1c71385f381b06f1cf8957fbac81c51df7415d4cc4a95eb56fb7c989': (1535,
                                                                                     '5af253bd1c71385f381b06f1cf8957fbac81c51df7415d4cc4a95eb56fb7c989'),
 'objects/sha256/5b8095a39c7e3f90c0ceac69c924e80b25ad4ee6249891eb9c45d1365df98ec9': (8451,
                                                                                     '5b8095a39c7e3f90c0ceac69c924e80b25ad4ee6249891eb9c45d1365df98ec9'),
 'objects/sha256/5c3ae9c2697e1cfab46a5495b8863eea84ba2c851c5badb1c7db5dd6de3e1a93': (159009,
                                                                                     '5c3ae9c2697e1cfab46a5495b8863eea84ba2c851c5badb1c7db5dd6de3e1a93'),
 'objects/sha256/5c83adf16728892cedc1e7c7ecfb8ec5342a3d5f4e807c76b7b9b7445c7f8fc1': (8632,
                                                                                     '5c83adf16728892cedc1e7c7ecfb8ec5342a3d5f4e807c76b7b9b7445c7f8fc1'),
 'objects/sha256/60209683c04233e1ca1da3be0b8a5e47d372e125bd90617330654dffca86e3c2': (467,
                                                                                     '60209683c04233e1ca1da3be0b8a5e47d372e125bd90617330654dffca86e3c2'),
 'objects/sha256/6039540b8150cd5463179e086ac87a96fc29fcc587b47830358c8d0a9bb97c9d': (2167,
                                                                                     '6039540b8150cd5463179e086ac87a96fc29fcc587b47830358c8d0a9bb97c9d'),
 'objects/sha256/607a9470e64932aaa0000b7e9d34b538c67319092ec3fef0635a084ce98fe0c1': (714,
                                                                                     '607a9470e64932aaa0000b7e9d34b538c67319092ec3fef0635a084ce98fe0c1'),
 'objects/sha256/60f7a12788a5cc7867e2b731b696392078cb08e961a8ce7d16612c34b0db00f0': (381,
                                                                                     '60f7a12788a5cc7867e2b731b696392078cb08e961a8ce7d16612c34b0db00f0'),
 'objects/sha256/6103df8147d93c97f04067ef500deff157ca6a0a8ac50668d3b40225a6d4479d': (279,
                                                                                     '6103df8147d93c97f04067ef500deff157ca6a0a8ac50668d3b40225a6d4479d'),
 'objects/sha256/61f12e52957a630c8a756d28f9a5e52a76c1de205b44b14d4ca03eb07b9327c0': (3943,
                                                                                     '61f12e52957a630c8a756d28f9a5e52a76c1de205b44b14d4ca03eb07b9327c0'),
 'objects/sha256/63f463fca4fc69afdd04181e5c0d5fe967d0aacd83165b17e5825d8c8dd97306': (571,
                                                                                     '63f463fca4fc69afdd04181e5c0d5fe967d0aacd83165b17e5825d8c8dd97306'),
 'objects/sha256/6484e8da364ffe59b9f659cdfd64716f672b28d82af6ca7f89b756946e3d8cf6': (35673,
                                                                                     '6484e8da364ffe59b9f659cdfd64716f672b28d82af6ca7f89b756946e3d8cf6'),
 'objects/sha256/660b028a189539907279f810038dfabb8990e23ab703e7ee4e249bc31eb730c0': (453,
                                                                                     '660b028a189539907279f810038dfabb8990e23ab703e7ee4e249bc31eb730c0'),
 'objects/sha256/673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1': (573,
                                                                                     '673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1'),
 'objects/sha256/67aabf6f36fb2a71e9cfa3ba52f225de328564f5bcc7b81f6d2218877e74a796': (1010,
                                                                                     '67aabf6f36fb2a71e9cfa3ba52f225de328564f5bcc7b81f6d2218877e74a796'),
 'objects/sha256/68a1de3fe16a185a62d9ccf82da75cdbc50d84b2c6aacf799ed223c19ce07ffc': (867,
                                                                                     '68a1de3fe16a185a62d9ccf82da75cdbc50d84b2c6aacf799ed223c19ce07ffc'),
 'objects/sha256/6aaa64fad0d8cde2920356c618e8b32b0ac3714923ac42359fd802b6b9d8f686': (152696,
                                                                                     '6aaa64fad0d8cde2920356c618e8b32b0ac3714923ac42359fd802b6b9d8f686'),
 'objects/sha256/6b134f1afbdf73ce73c22c5e0bc79e77246b2b247a37c9e5b95f305115f96626': (2795,
                                                                                     '6b134f1afbdf73ce73c22c5e0bc79e77246b2b247a37c9e5b95f305115f96626'),
 'objects/sha256/6b4f333973769fd2ec033da493a6af85dbd8e4fe6615a287e2a057c465d63406': (2504332,
                                                                                     '6b4f333973769fd2ec033da493a6af85dbd8e4fe6615a287e2a057c465d63406'),
 'objects/sha256/6befbf43a4aa65e3274e1df054130d3623951582687725e005dd7ac5fc0f305f': (8300,
                                                                                     '6befbf43a4aa65e3274e1df054130d3623951582687725e005dd7ac5fc0f305f'),
 'objects/sha256/6cb90d8685f2824af33f1ccb2889aa5ed36a6bec4a87d1763099e00d41c7d1bf': (415328,
                                                                                     '6cb90d8685f2824af33f1ccb2889aa5ed36a6bec4a87d1763099e00d41c7d1bf'),
 'objects/sha256/6cc3b1e9ae55933356386b0bbd67922ba62e5ab232ffdd67cfa2491318396ed6': (1570,
                                                                                     '6cc3b1e9ae55933356386b0bbd67922ba62e5ab232ffdd67cfa2491318396ed6'),
 'objects/sha256/6dd4bd2994ad425576794eb13c6eb853877faad348a92156f07c6139daeec8b8': (9210,
                                                                                     '6dd4bd2994ad425576794eb13c6eb853877faad348a92156f07c6139daeec8b8'),
 'objects/sha256/6e2a781da1029f5786f88c0978b04133bf215ae23a0a8ddd2466416e264e6668': (165,
                                                                                     '6e2a781da1029f5786f88c0978b04133bf215ae23a0a8ddd2466416e264e6668'),
 'objects/sha256/6ff59bd0026383540c6a7e191d113830eeac18d3de9e84866b557f27eea5f28f': (117,
                                                                                     '6ff59bd0026383540c6a7e191d113830eeac18d3de9e84866b557f27eea5f28f'),
 'objects/sha256/7008da1de17172aa71fc9c42062117aab1fda557104b43a36d3085723082fbc4': (782,
                                                                                     '7008da1de17172aa71fc9c42062117aab1fda557104b43a36d3085723082fbc4'),
 'objects/sha256/704ab558a25e69fc17aecfe056fa4130f8d12d717469786776c07780a84c2b2a': (12275,
                                                                                     '704ab558a25e69fc17aecfe056fa4130f8d12d717469786776c07780a84c2b2a'),
 'objects/sha256/7085d14c2e40cff60a203a2494ac37ab45b2c20dc34d8773f77bb696b2760a50': (2707,
                                                                                     '7085d14c2e40cff60a203a2494ac37ab45b2c20dc34d8773f77bb696b2760a50'),
 'objects/sha256/70dc0fd9393d9be032abab7b8f42baaf85b8847bdc607d419cb00d409426543b': (26454,
                                                                                     '70dc0fd9393d9be032abab7b8f42baaf85b8847bdc607d419cb00d409426543b'),
 'objects/sha256/7135f4958e404469a335ffdc5a364154b67284fdfa01380b0873d81e53fb469d': (5724,
                                                                                     '7135f4958e404469a335ffdc5a364154b67284fdfa01380b0873d81e53fb469d'),
 'objects/sha256/71be52bc9d75bde41b3e545b5936d242f23ed09dbf9e94cf098a506614b1954c': (159135,
                                                                                     '71be52bc9d75bde41b3e545b5936d242f23ed09dbf9e94cf098a506614b1954c'),
 'objects/sha256/72c4bae991d94eb74033bbcdc695d19b05b775d5632710ffe38c8bb9b3b5876c': (298,
                                                                                     '72c4bae991d94eb74033bbcdc695d19b05b775d5632710ffe38c8bb9b3b5876c'),
 'objects/sha256/73c378f364ce797983719ba73005420efc6b48c516ea8258daf59d56dbf3e6b0': (8544,
                                                                                     '73c378f364ce797983719ba73005420efc6b48c516ea8258daf59d56dbf3e6b0'),
 'objects/sha256/753353a19af9cb1dbdd560b89b6613017b8c8fb2feecbd9783eded505de49df8': (1054,
                                                                                     '753353a19af9cb1dbdd560b89b6613017b8c8fb2feecbd9783eded505de49df8'),
 'objects/sha256/7632a905eb4c264a2521412efba5cad6dba9d847f17ca5494d8f713b2d1865db': (18454,
                                                                                     '7632a905eb4c264a2521412efba5cad6dba9d847f17ca5494d8f713b2d1865db'),
 'objects/sha256/76a9b86af67069dae1cac2e8128965305df73ccfc403612d5294b16a0a6f9f33': (1153045,
                                                                                     '76a9b86af67069dae1cac2e8128965305df73ccfc403612d5294b16a0a6f9f33'),
 'objects/sha256/7769ee31c3e229793f5c7506ee521d1dd2abe03cd173182021289bc59e85bf92': (3475,
                                                                                     '7769ee31c3e229793f5c7506ee521d1dd2abe03cd173182021289bc59e85bf92'),
 'objects/sha256/77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b': (139308,
                                                                                     '77e30cac714c74c01a143ebf9976029d6d56a167390eab51c07d12ddde043f3b'),
 'objects/sha256/7a544d86f0f96d6ce22f08845eba43894b115a31b6e7ce91c00e7eede899a845': (2825,
                                                                                     '7a544d86f0f96d6ce22f08845eba43894b115a31b6e7ce91c00e7eede899a845'),
 'objects/sha256/7ab87b55707e2ec8e05b6fd6a0f3fde3561b3cd8dd7fdb5839ef9469530f1bf5': (9210,
                                                                                     '7ab87b55707e2ec8e05b6fd6a0f3fde3561b3cd8dd7fdb5839ef9469530f1bf5'),
 'objects/sha256/7af2a312e23f6cd27d199eab64f873565d8c39c0540d13f26a95bb7f11338bc5': (16877,
                                                                                     '7af2a312e23f6cd27d199eab64f873565d8c39c0540d13f26a95bb7f11338bc5'),
 'objects/sha256/7be913679730c7b84df5683876c82473d4045556f1ba2fbd997817c3fa683414': (122732,
                                                                                     '7be913679730c7b84df5683876c82473d4045556f1ba2fbd997817c3fa683414'),
 'objects/sha256/7d1220582dacd2c46cb7205206463b99a2655c20d1b52bede27bc01458f23231': (430820,
                                                                                     '7d1220582dacd2c46cb7205206463b99a2655c20d1b52bede27bc01458f23231'),
 'objects/sha256/7daeab6a74ac46aeebb7f9ad203f4099838a3f0146ef8af3d8647b4484cd1f85': (86629,
                                                                                     '7daeab6a74ac46aeebb7f9ad203f4099838a3f0146ef8af3d8647b4484cd1f85'),
 'objects/sha256/7eb489b2ca1cb86b0a366b75bd6dfd2ea3de736e903bb6203f289306695636fb': (3565,
                                                                                     '7eb489b2ca1cb86b0a366b75bd6dfd2ea3de736e903bb6203f289306695636fb'),
 'objects/sha256/7fedf302eaf3f399993a5166c04373f35093ef9cf77ba6076e2311065ad86220': (1801,
                                                                                     '7fedf302eaf3f399993a5166c04373f35093ef9cf77ba6076e2311065ad86220'),
 'objects/sha256/81afad712acd8f169c697b1e97b24c5a8df84ab7425a318b34a3149619cf4314': (2486588,
                                                                                     '81afad712acd8f169c697b1e97b24c5a8df84ab7425a318b34a3149619cf4314'),
 'objects/sha256/82e26283f881ebaa50f9cf12be27b109303db1c229d3c12d5145d868a7937d4a': (8814,
                                                                                     '82e26283f881ebaa50f9cf12be27b109303db1c229d3c12d5145d868a7937d4a'),
 'objects/sha256/82f7fdbff6fb90c03c408ef772f3510267a1debc76986e4dfff57582165e8876': (314985,
                                                                                     '82f7fdbff6fb90c03c408ef772f3510267a1debc76986e4dfff57582165e8876'),
 'objects/sha256/8318ab3f3c1e5ef1b92786dcaeb7cb6b81f020d6c37e8e1723e47cb490527196': (2769,
                                                                                     '8318ab3f3c1e5ef1b92786dcaeb7cb6b81f020d6c37e8e1723e47cb490527196'),
 'objects/sha256/83fcb789af7d21840e035e1d045a2fc07918977317d470a31a9bc345c6c67a86': (24979,
                                                                                     '83fcb789af7d21840e035e1d045a2fc07918977317d470a31a9bc345c6c67a86'),
 'objects/sha256/86bf7590a46fa149d36ab036850b4a9bcf126dfb05b9dc6bcd451d622ceccf94': (4259,
                                                                                     '86bf7590a46fa149d36ab036850b4a9bcf126dfb05b9dc6bcd451d622ceccf94'),
 'objects/sha256/8be246a710f8068e3b140791b9518fa5dd9e5c2411fbadfc7efc53e824ded0f4': (152690,
                                                                                     '8be246a710f8068e3b140791b9518fa5dd9e5c2411fbadfc7efc53e824ded0f4'),
 'objects/sha256/8cc861d3709007ee300361198696ad32e659dc56aef2be43c28dc59ae3706952': (32,
                                                                                     '8cc861d3709007ee300361198696ad32e659dc56aef2be43c28dc59ae3706952'),
 'objects/sha256/8e85f14861c73cad18b052342acbe5e8a2153a038e95db68da20d8d50d188998': (41515,
                                                                                     '8e85f14861c73cad18b052342acbe5e8a2153a038e95db68da20d8d50d188998'),
 'objects/sha256/8ef587a667614c6cc504657faee1b9ad75a9cda1dea9156e0daab40774c1ced9': (562,
                                                                                     '8ef587a667614c6cc504657faee1b9ad75a9cda1dea9156e0daab40774c1ced9'),
 'objects/sha256/909d1b80e0762d71a36c7b89b00c8f0769674e62c4c67a69ba46e335fad68e8e': (319,
                                                                                     '909d1b80e0762d71a36c7b89b00c8f0769674e62c4c67a69ba46e335fad68e8e'),
 'objects/sha256/916094256c35ef31404d938035558878d4499460da35015991f4e7a714208751': (779,
                                                                                     '916094256c35ef31404d938035558878d4499460da35015991f4e7a714208751'),
 'objects/sha256/91d8bae1eddca2ac723a08e31f76f17f2cf7a71974145b6c9ae41746b079a4ae': (434515,
                                                                                     '91d8bae1eddca2ac723a08e31f76f17f2cf7a71974145b6c9ae41746b079a4ae'),
 'objects/sha256/93a5b884f4b1266775c2b1a77291f69ade9f2a39cedf66550d06a2f971c70f04': (355288,
                                                                                     '93a5b884f4b1266775c2b1a77291f69ade9f2a39cedf66550d06a2f971c70f04'),
 'objects/sha256/93e7fb31931b9d0cf42dd0d7e5362c6a447a9999b5ab6640ee4757c17abc0ecf': (4083,
                                                                                     '93e7fb31931b9d0cf42dd0d7e5362c6a447a9999b5ab6640ee4757c17abc0ecf'),
 'objects/sha256/94c3611c2b519280891a12bf73c90c514fabe56aa168ad29870682e52fab4d49': (2423,
                                                                                     '94c3611c2b519280891a12bf73c90c514fabe56aa168ad29870682e52fab4d49'),
 'objects/sha256/973fef76b4adee451f50269d279a39cfe282506d4241cb9b28c6cc97a284a5b7': (3943,
                                                                                     '973fef76b4adee451f50269d279a39cfe282506d4241cb9b28c6cc97a284a5b7'),
 'objects/sha256/9a469a57df2f5e4b18c06f707ada2e0e69eaca7cb1f1f299450300c1b361c984': (2078,
                                                                                     '9a469a57df2f5e4b18c06f707ada2e0e69eaca7cb1f1f299450300c1b361c984'),
 'objects/sha256/9ad280da99096cc692ac882854a96e3a0285ceb0ebce9e49a5da6bba7b347f1d': (470,
                                                                                     '9ad280da99096cc692ac882854a96e3a0285ceb0ebce9e49a5da6bba7b347f1d'),
 'objects/sha256/9aeff3344a9d236bfaca7aa42f02e90e589e13cf665f5e7ad63171b1acb82c1b': (2114,
                                                                                     '9aeff3344a9d236bfaca7aa42f02e90e589e13cf665f5e7ad63171b1acb82c1b'),
 'objects/sha256/9b1461f638e3ad6d684b47f69a5073354dca3e80214faab9493165429c9700df': (16475,
                                                                                     '9b1461f638e3ad6d684b47f69a5073354dca3e80214faab9493165429c9700df'),
 'objects/sha256/9b1a4b71f6f81f99ba8d8e67d020b45ed302eb410d023468660cd1168e3945e1': (58068,
                                                                                     '9b1a4b71f6f81f99ba8d8e67d020b45ed302eb410d023468660cd1168e3945e1'),
 'objects/sha256/9b1b98e64e321b1afd8dc1e90c8f16b1061f5e92acb78135a4e5951c8a361869': (5158,
                                                                                     '9b1b98e64e321b1afd8dc1e90c8f16b1061f5e92acb78135a4e5951c8a361869'),
 'objects/sha256/9b9dafbbc75af63ae09e581b18c5404f3e3bac785324498a410d7b5e77355e28': (10444,
                                                                                     '9b9dafbbc75af63ae09e581b18c5404f3e3bac785324498a410d7b5e77355e28'),
 'objects/sha256/9bfa6b65e2ebd26be28a90ef300e3624070cfd3abf8b2244e5506c881b8564a4': (5652,
                                                                                     '9bfa6b65e2ebd26be28a90ef300e3624070cfd3abf8b2244e5506c881b8564a4'),
 'objects/sha256/9c7f5f7232423ee9e45fd4f793facd648a13ed0040fef381d04292c34d48781c': (5665,
                                                                                     '9c7f5f7232423ee9e45fd4f793facd648a13ed0040fef381d04292c34d48781c'),
 'objects/sha256/9e357bbc323201e2d06d33bda29d52ca4e64432b2e988a03b334dd6e21e4691c': (8597,
                                                                                     '9e357bbc323201e2d06d33bda29d52ca4e64432b2e988a03b334dd6e21e4691c'),
 'objects/sha256/9f048435866d641e0dc387b8b2b308b8c5c2131631eee35cc676d5c2c7deaeca': (847,
                                                                                     '9f048435866d641e0dc387b8b2b308b8c5c2131631eee35cc676d5c2c7deaeca'),
 'objects/sha256/9f5f6f3e29f28a9447a3e9f6fa0d6ced1071c8658854f40800e13c587a55c081': (5230,
                                                                                     '9f5f6f3e29f28a9447a3e9f6fa0d6ced1071c8658854f40800e13c587a55c081'),
 'objects/sha256/a001a7f17ed407c8c073ef6b6cb6bcc57605bc7b7803017cd83018273767de74': (26205,
                                                                                     'a001a7f17ed407c8c073ef6b6cb6bcc57605bc7b7803017cd83018273767de74'),
 'objects/sha256/a20f6dffc27545837d8399f390263057141df5690dc84ebf219367747ff17148': (7764,
                                                                                     'a20f6dffc27545837d8399f390263057141df5690dc84ebf219367747ff17148'),
 'objects/sha256/a341fe3c23f40be3b422df946cc664aad9d6d0cce1386c51e90744d805e61689': (117647,
                                                                                     'a341fe3c23f40be3b422df946cc664aad9d6d0cce1386c51e90744d805e61689'),
 'objects/sha256/a386342628384061e21f41943b8bc29f3f0a2389cdcc12301b46d2c93a85f3e9': (355426,
                                                                                     'a386342628384061e21f41943b8bc29f3f0a2389cdcc12301b46d2c93a85f3e9'),
 'objects/sha256/a5952266914ef664bc0c61b3363250ec83ccf65631572d2366cd6a3b2e2f5533': (1304,
                                                                                     'a5952266914ef664bc0c61b3363250ec83ccf65631572d2366cd6a3b2e2f5533'),
 'objects/sha256/a60639dfa9212cd05f843c0c03dc6c0f1f55b570094ea1d9823435bd879bf5cc': (18363,
                                                                                     'a60639dfa9212cd05f843c0c03dc6c0f1f55b570094ea1d9823435bd879bf5cc'),
 'objects/sha256/a6b05364d9d6d47f088d77dd9cba49d29c1e37ac23948c31c29ec06383554d30': (9210,
                                                                                     'a6b05364d9d6d47f088d77dd9cba49d29c1e37ac23948c31c29ec06383554d30'),
 'objects/sha256/a775033c86a8d23840e33ca44841b162801e1ec9db5ad16d392d626611ecd07a': (83020,
                                                                                     'a775033c86a8d23840e33ca44841b162801e1ec9db5ad16d392d626611ecd07a'),
 'objects/sha256/a7bdbc8ee8873a1a9b4a86ba3ef4b617a593cae3a4225c1c10c41f413a30ed14': (261,
                                                                                     'a7bdbc8ee8873a1a9b4a86ba3ef4b617a593cae3a4225c1c10c41f413a30ed14'),
 'objects/sha256/a7cdce5a428e7975a4879bca8e157f476cb45c311eee6898f19a262f66c39f93': (373,
                                                                                     'a7cdce5a428e7975a4879bca8e157f476cb45c311eee6898f19a262f66c39f93'),
 'objects/sha256/a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f': (3905,
                                                                                     'a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f'),
 'objects/sha256/a8e636b7f95580714275394e1a814bc49cae7f25011d749631f21ba2b30c6684': (1307,
                                                                                     'a8e636b7f95580714275394e1a814bc49cae7f25011d749631f21ba2b30c6684'),
 'objects/sha256/a97e5fa1eb42162148b798f08f1b1fe5b35b0f52028b4d4da7e87e0ee14f4c8b': (1007,
                                                                                     'a97e5fa1eb42162148b798f08f1b1fe5b35b0f52028b4d4da7e87e0ee14f4c8b'),
 'objects/sha256/aa1f8020920266ca8e26c491a7d8db03d98515ac4c6259dd9da36ef717c44391': (9210,
                                                                                     'aa1f8020920266ca8e26c491a7d8db03d98515ac4c6259dd9da36ef717c44391'),
 'objects/sha256/aab258b380bb5cf3920944719c230d228b03499e66c9d0d87f12fa14b7fed72a': (8869,
                                                                                     'aab258b380bb5cf3920944719c230d228b03499e66c9d0d87f12fa14b7fed72a'),
 'objects/sha256/aab566a75aa8b4a4105ce0e5d3fb241e52b25d8d04260a34d088d8216e703f7f': (1336,
                                                                                     'aab566a75aa8b4a4105ce0e5d3fb241e52b25d8d04260a34d088d8216e703f7f'),
 'objects/sha256/ac33b467c71bc931992bf14669cdaa073ecb5725906e8ae393634d6578c8aef5': (864,
                                                                                     'ac33b467c71bc931992bf14669cdaa073ecb5725906e8ae393634d6578c8aef5'),
 'objects/sha256/ac9eb8201d90a09df2e112d610b46e0be9213db370e734f2f919e4204b513ffb': (318092,
                                                                                     'ac9eb8201d90a09df2e112d610b46e0be9213db370e734f2f919e4204b513ffb'),
 'objects/sha256/acbfcded1243f9b93c0ba1b9610d771618a327544c397924a1334d4e1dd2c1be': (8516,
                                                                                     'acbfcded1243f9b93c0ba1b9610d771618a327544c397924a1334d4e1dd2c1be'),
 'objects/sha256/ad2960ea9a277bc2ce0fba14a6483c6f36579730bb98b39ada496e58e84df141': (8822,
                                                                                     'ad2960ea9a277bc2ce0fba14a6483c6f36579730bb98b39ada496e58e84df141'),
 'objects/sha256/aef2e384808baa3d53718f146b45e131766d05fc8747cc4d58943299108d6530': (14058,
                                                                                     'aef2e384808baa3d53718f146b45e131766d05fc8747cc4d58943299108d6530'),
 'objects/sha256/afb3618a45f66f11beea51a33b374a8b119d770f99b10f41e1720e5e2e94dc35': (3763,
                                                                                     'afb3618a45f66f11beea51a33b374a8b119d770f99b10f41e1720e5e2e94dc35'),
 'objects/sha256/b0c7863e527a65f89cf97f62eb30dc3025b28395bdbe36b4b85b1f66f458d852': (381,
                                                                                     'b0c7863e527a65f89cf97f62eb30dc3025b28395bdbe36b4b85b1f66f458d852'),
 'objects/sha256/b1deb18577ef914d4c61bdabbedab7235d316b516fcc1495ab6b04cc61d52d49': (1035,
                                                                                     'b1deb18577ef914d4c61bdabbedab7235d316b516fcc1495ab6b04cc61d52d49'),
 'objects/sha256/b25011942643c187ef8f21012c4f46f5d0d7657a850e8839bf231af192957ae0': (641,
                                                                                     'b25011942643c187ef8f21012c4f46f5d0d7657a850e8839bf231af192957ae0'),
 'objects/sha256/b464ff6312c3f5355f98f899f393edcf0f420b27912f6b560f1b827fc02bffd8': (558,
                                                                                     'b464ff6312c3f5355f98f899f393edcf0f420b27912f6b560f1b827fc02bffd8'),
 'objects/sha256/b58c39b301728d43d8eea7a793b5e3f3f98880e5acede356c00c6dc5bebb7693': (958,
                                                                                     'b58c39b301728d43d8eea7a793b5e3f3f98880e5acede356c00c6dc5bebb7693'),
 'objects/sha256/b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065': (3895,
                                                                                     'b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065'),
 'objects/sha256/b727fa531c1a244a1547378c5a5e5bca7be54464fa714ccc805045a8f0613e88': (8309,
                                                                                     'b727fa531c1a244a1547378c5a5e5bca7be54464fa714ccc805045a8f0613e88'),
 'objects/sha256/b8479a28e90448d619b9d63987473ebd0c3e57c25cf7847afd8e552a94466f57': (333,
                                                                                     'b8479a28e90448d619b9d63987473ebd0c3e57c25cf7847afd8e552a94466f57'),
 'objects/sha256/b893837e26741a51510e2c9087f0f521c3bcc7847d36ac708ec9ddb0be36393d': (7409,
                                                                                     'b893837e26741a51510e2c9087f0f521c3bcc7847d36ac708ec9ddb0be36393d'),
 'objects/sha256/b898ec38a0c10b5e213d64f49a27c93f2c0ce2a2a8cf77f0fedfa47a3dd19a7b': (15739,
                                                                                     'b898ec38a0c10b5e213d64f49a27c93f2c0ce2a2a8cf77f0fedfa47a3dd19a7b'),
 'objects/sha256/b90bbec3242c3bce33fa5cbce8030c9fa437d419b5efd82cc9bbc39c7509560e': (26713,
                                                                                     'b90bbec3242c3bce33fa5cbce8030c9fa437d419b5efd82cc9bbc39c7509560e'),
 'objects/sha256/b9a03d8954c4d5576093641b9772e558205fb54c823fe364db43ba9c315cc702': (491,
                                                                                     'b9a03d8954c4d5576093641b9772e558205fb54c823fe364db43ba9c315cc702'),
 'objects/sha256/bacd19d9ac14f418c5b460937d100320688d9f1ce5bf5e900a50fa7708b0b967': (2707,
                                                                                     'bacd19d9ac14f418c5b460937d100320688d9f1ce5bf5e900a50fa7708b0b967'),
 'objects/sha256/bb82d668e185f8fa500d159674f63c9bf058eb67af0b8ae3a9d67a0d3c18f7ee': (8521,
                                                                                     'bb82d668e185f8fa500d159674f63c9bf058eb67af0b8ae3a9d67a0d3c18f7ee'),
 'objects/sha256/bb845c3be48f36a50c2677de9566fd9cbc99c6c710cc57de4f7394b7f0a66036': (245,
                                                                                     'bb845c3be48f36a50c2677de9566fd9cbc99c6c710cc57de4f7394b7f0a66036'),
 'objects/sha256/bda25a2f047af04626be126cd42f9e6b995ee476ad4b94ac47d3a528a6f4cea9': (38,
                                                                                     'bda25a2f047af04626be126cd42f9e6b995ee476ad4b94ac47d3a528a6f4cea9'),
 'objects/sha256/bf200dcf4d5d10be840b843a3e5b85e5a3de237ec6574a754c50674ad52aeea3': (1388,
                                                                                     'bf200dcf4d5d10be840b843a3e5b85e5a3de237ec6574a754c50674ad52aeea3'),
 'objects/sha256/c07938090c7fd2463099af8d94f5b500d12405430ea4ff9109dedf22959bc81a': (1153385,
                                                                                     'c07938090c7fd2463099af8d94f5b500d12405430ea4ff9109dedf22959bc81a'),
 'objects/sha256/c0a18d997e27e162c1db1781fd678679cc6012d54a0ac304beb2588359971fc3': (2825,
                                                                                     'c0a18d997e27e162c1db1781fd678679cc6012d54a0ac304beb2588359971fc3'),
 'objects/sha256/c0e7abca473bc33713b9c78f02374573d65e3b6fd654777464833baa6b92b067': (209,
                                                                                     'c0e7abca473bc33713b9c78f02374573d65e3b6fd654777464833baa6b92b067'),
 'objects/sha256/c0f2f1f93784b60cc3bfcb8d868ea49c09a6c2489cb1bae2b43b8b8494b599ac': (34335,
                                                                                     'c0f2f1f93784b60cc3bfcb8d868ea49c09a6c2489cb1bae2b43b8b8494b599ac'),
 'objects/sha256/c2fbb183e88d727edce88e4b8b4610d9504436527e1a8ffe7793ce0bde156ec7': (3419,
                                                                                     'c2fbb183e88d727edce88e4b8b4610d9504436527e1a8ffe7793ce0bde156ec7'),
 'objects/sha256/c341672d7808d83c24e695b4101354b5bf4819a074c32c6e42834a4c6b7b96b2': (2580,
                                                                                     'c341672d7808d83c24e695b4101354b5bf4819a074c32c6e42834a4c6b7b96b2'),
 'objects/sha256/c3eee81ae4d5d75575bc14156435b8e63851783e73435313b5f92e757e1765a5': (568,
                                                                                     'c3eee81ae4d5d75575bc14156435b8e63851783e73435313b5f92e757e1765a5'),
 'objects/sha256/c451faa4b93628ac2826f1c60644da7802f95689d5e1c1b917353d7e0baad91d': (3517,
                                                                                     'c451faa4b93628ac2826f1c60644da7802f95689d5e1c1b917353d7e0baad91d'),
 'objects/sha256/c4781fc6064eded95fcf4e60e9888a93f794efd17c63969e9c31853236f88d01': (1963,
                                                                                     'c4781fc6064eded95fcf4e60e9888a93f794efd17c63969e9c31853236f88d01'),
 'objects/sha256/c51486fa67aa86d818062c09fe71bc14743face979d28b2233455752bffaa1c5': (471,
                                                                                     'c51486fa67aa86d818062c09fe71bc14743face979d28b2233455752bffaa1c5'),
 'objects/sha256/c6049d18eddde3a5b57ed4418b3cb5eefd6a57c34b21d45579035b928f7cdeed': (106151,
                                                                                     'c6049d18eddde3a5b57ed4418b3cb5eefd6a57c34b21d45579035b928f7cdeed'),
 'objects/sha256/c6c99b5013d92da78f9ca758fd98fa7946540e544bbb2e06321af5f162d151be': (1243,
                                                                                     'c6c99b5013d92da78f9ca758fd98fa7946540e544bbb2e06321af5f162d151be'),
 'objects/sha256/c84ab5fd54f80243aeeaa3b25f443a1688170ab2e15b5613ae425345bc0142a7': (380,
                                                                                     'c84ab5fd54f80243aeeaa3b25f443a1688170ab2e15b5613ae425345bc0142a7'),
 'objects/sha256/ca1e5b3f97e1b88b28036151d02191d7abea98a5ebc4fe7f46401f6338ada909': (898,
                                                                                     'ca1e5b3f97e1b88b28036151d02191d7abea98a5ebc4fe7f46401f6338ada909'),
 'objects/sha256/ca2744ff13c868de7712c9993602b4aa8ce100b76e83ae8557b6e9c8e8069cff': (33,
                                                                                     'ca2744ff13c868de7712c9993602b4aa8ce100b76e83ae8557b6e9c8e8069cff'),
 'objects/sha256/cabf397f58cad0ad596ded5710ad94085955d41525b1e5d1a43e669c7e443752': (145,
                                                                                     'cabf397f58cad0ad596ded5710ad94085955d41525b1e5d1a43e669c7e443752'),
 'objects/sha256/cb1c0aa0ce6b7689bb5ccc1d6ba2fa62e6fe19878978a74db3c89a231849fbcf': (11368,
                                                                                     'cb1c0aa0ce6b7689bb5ccc1d6ba2fa62e6fe19878978a74db3c89a231849fbcf'),
 'objects/sha256/cd0d355bd365702baed692bcd362f10c7403e2a7636ba859da395679a44a0b1e': (15895,
                                                                                     'cd0d355bd365702baed692bcd362f10c7403e2a7636ba859da395679a44a0b1e'),
 'objects/sha256/cd8a989a5525191271f48e8e86631ad5df97e1b32126404c06c8bfdc0355ac1b': (592,
                                                                                     'cd8a989a5525191271f48e8e86631ad5df97e1b32126404c06c8bfdc0355ac1b'),
 'objects/sha256/cd97e3f2cc53bb0b52ebe29005a1e334f6f3de19c344c85d35b6a76ac441806c': (2486807,
                                                                                     'cd97e3f2cc53bb0b52ebe29005a1e334f6f3de19c344c85d35b6a76ac441806c'),
 'objects/sha256/ce06b28274305dd73dfe52d406c22cf2864ae2a410c604fee82c4685d9edbcb0': (64444,
                                                                                     'ce06b28274305dd73dfe52d406c22cf2864ae2a410c604fee82c4685d9edbcb0'),
 'objects/sha256/cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a': (6813,
                                                                                     'cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a'),
 'objects/sha256/cf13eef034caabd6924be51dafb3cb0b6487538bb4668f735cb0d910da26ba76': (3517,
                                                                                     'cf13eef034caabd6924be51dafb3cb0b6487538bb4668f735cb0d910da26ba76'),
 'objects/sha256/cf237d72a71f20fd74993f56a3774925abf9960adb41ca6d2b4263b723b9d35e': (496,
                                                                                     'cf237d72a71f20fd74993f56a3774925abf9960adb41ca6d2b4263b723b9d35e'),
 'objects/sha256/cfc743daaec5db90cb9445969f3e338668c607bbe955446e438dbfff1049df52': (1581,
                                                                                     'cfc743daaec5db90cb9445969f3e338668c607bbe955446e438dbfff1049df52'),
 'objects/sha256/cfe2fb883e45ab00b754733d418edbba639fa404383585d740dfa40123d0dc53': (1057,
                                                                                     'cfe2fb883e45ab00b754733d418edbba639fa404383585d740dfa40123d0dc53'),
 'objects/sha256/d0225feb6311753bbeda7387fe2e8fe61aabd00480ed7ab71349eb853b1606da': (19926,
                                                                                     'd0225feb6311753bbeda7387fe2e8fe61aabd00480ed7ab71349eb853b1606da'),
 'objects/sha256/d063ec43f4c838284a0ae7408da8cab2518b37426739cba4cf2e49d1dd1f0b5b': (466,
                                                                                     'd063ec43f4c838284a0ae7408da8cab2518b37426739cba4cf2e49d1dd1f0b5b'),
 'objects/sha256/d12698294b69ebabadb23a0f8c2642516b8935d2f8081c48cd8d826f111212bb': (107677,
                                                                                     'd12698294b69ebabadb23a0f8c2642516b8935d2f8081c48cd8d826f111212bb'),
 'objects/sha256/d1795e0d25c601a50e127659b959b65add062fbe154a6f48611203c65ea2ff77': (176534,
                                                                                     'd1795e0d25c601a50e127659b959b65add062fbe154a6f48611203c65ea2ff77'),
 'objects/sha256/d1ccba298c06ac53eb9ce70c51ac3a09b7d5bfec39d156bf55a07588a01fb95c': (260,
                                                                                     'd1ccba298c06ac53eb9ce70c51ac3a09b7d5bfec39d156bf55a07588a01fb95c'),
 'objects/sha256/d2e9699cf6f6f4d9186846952b407b380c64006adf4ed955b830a474c319bd24': (2138,
                                                                                     'd2e9699cf6f6f4d9186846952b407b380c64006adf4ed955b830a474c319bd24'),
 'objects/sha256/d58620f342f781481c9d6ce11030c432abe48779ece6caafe2e6c6efdb73bbf6': (26218,
                                                                                     'd58620f342f781481c9d6ce11030c432abe48779ece6caafe2e6c6efdb73bbf6'),
 'objects/sha256/d718b60830df1f5f74d6952cb811d839889c40edbbbb0b098f8596752d00702d': (4183,
                                                                                     'd718b60830df1f5f74d6952cb811d839889c40edbbbb0b098f8596752d00702d'),
 'objects/sha256/d7f6a669e439f451c0ca112a654e696f48f63b896e373f2b147613034074d855': (12329,
                                                                                     'd7f6a669e439f451c0ca112a654e696f48f63b896e373f2b147613034074d855'),
 'objects/sha256/d9d753ca22edaadbde823ddfdf3c1407499cd74a4595bd15a7e473d19dfdb413': (3046,
                                                                                     'd9d753ca22edaadbde823ddfdf3c1407499cd74a4595bd15a7e473d19dfdb413'),
 'objects/sha256/dab636461967b24168c71f06b69cce4a06e7fcc89f575ed723567f59bda41e71': (1903,
                                                                                     'dab636461967b24168c71f06b69cce4a06e7fcc89f575ed723567f59bda41e71'),
 'objects/sha256/dabcf94b721a656994fc24d620452adc2789eacd6dbfbbf9e73a0aed4aed0e8f': (9210,
                                                                                     'dabcf94b721a656994fc24d620452adc2789eacd6dbfbbf9e73a0aed4aed0e8f'),
 'objects/sha256/db991c1b5e11f8ac5491b227d9fb5113299a5e21c068aa83ef723c2abe28506a': (360,
                                                                                     'db991c1b5e11f8ac5491b227d9fb5113299a5e21c068aa83ef723c2abe28506a'),
 'objects/sha256/dbadff5a978f1e3cabdd9dfa738e5b1259834cb1448916583d54ae9ad59e16d9': (2152,
                                                                                     'dbadff5a978f1e3cabdd9dfa738e5b1259834cb1448916583d54ae9ad59e16d9'),
 'objects/sha256/dc7f4d462ec9aad4614a2591c23c8ec100c73e0ab5c0b9b4582e05e3bc699431': (360,
                                                                                     'dc7f4d462ec9aad4614a2591c23c8ec100c73e0ab5c0b9b4582e05e3bc699431'),
 'objects/sha256/dd0d2b463fa4048a7dad6fd4e67cfb192d9010bd7c7921c3e5a0c01126e60768': (9210,
                                                                                     'dd0d2b463fa4048a7dad6fd4e67cfb192d9010bd7c7921c3e5a0c01126e60768'),
 'objects/sha256/dd74fc46a6f6a924cbd1c95b670083a10ee3a8c861351c78ce8a8b4b7e14d332': (834,
                                                                                     'dd74fc46a6f6a924cbd1c95b670083a10ee3a8c861351c78ce8a8b4b7e14d332'),
 'objects/sha256/de4f2ccd3e66270e3dc49c716ce08d18bdec40669b0eee8533794f6196d7aae7': (19125,
                                                                                     'de4f2ccd3e66270e3dc49c716ce08d18bdec40669b0eee8533794f6196d7aae7'),
 'objects/sha256/de547f194c9efa03e67220bec0735800d3affd8d959b5305f44c68df39c524b6': (24152,
                                                                                     'de547f194c9efa03e67220bec0735800d3affd8d959b5305f44c68df39c524b6'),
 'objects/sha256/ded1155488e610b95bbb588d8cd52854a66decff5214db67317bac094aadf709': (46,
                                                                                     'ded1155488e610b95bbb588d8cd52854a66decff5214db67317bac094aadf709'),
 'objects/sha256/df64ad6be8416f624e42623ae3b99a1a6a50b6827ada0c7a0eb78f91530cd67b': (8544,
                                                                                     'df64ad6be8416f624e42623ae3b99a1a6a50b6827ada0c7a0eb78f91530cd67b'),
 'objects/sha256/e06580217479f893051006715cd9a08713c1887b4c69f126ca96010c1ff7e7a6': (758,
                                                                                     'e06580217479f893051006715cd9a08713c1887b4c69f126ca96010c1ff7e7a6'),
 'objects/sha256/e1bb9fd1117c70ce6a14d34e63b3525715e399cbb1aa90348f39ae84311ba25b': (4247,
                                                                                     'e1bb9fd1117c70ce6a14d34e63b3525715e399cbb1aa90348f39ae84311ba25b'),
 'objects/sha256/e1d54893ef5aa9e977d7e34b72a90838d1932aeff018e1c9c9fa5d585735e2d5': (10410,
                                                                                     'e1d54893ef5aa9e977d7e34b72a90838d1932aeff018e1c9c9fa5d585735e2d5'),
 'objects/sha256/e462712d120d91d0f6c902b6aeb5377e6667b58a3450b7fd43a1170ec7fc91ae': (11475,
                                                                                     'e462712d120d91d0f6c902b6aeb5377e6667b58a3450b7fd43a1170ec7fc91ae'),
 'objects/sha256/e4b87d02f722fb4568f41d5c3158a1a7099f5ba940a33752f99ad38bec5de25f': (239789,
                                                                                     'e4b87d02f722fb4568f41d5c3158a1a7099f5ba940a33752f99ad38bec5de25f'),
 'objects/sha256/e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453': (10046,
                                                                                     'e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453'),
 'objects/sha256/e5243a8d7ed9a1f9b4d4c09ac74abf9b51b143d80b5505bb1403338e3bb569f5': (5437,
                                                                                     'e5243a8d7ed9a1f9b4d4c09ac74abf9b51b143d80b5505bb1403338e3bb569f5'),
 'objects/sha256/e5b445fc149e96d3039d56baed2da9f89d45bbd673f340ca7898296adc0e9c97': (147,
                                                                                     'e5b445fc149e96d3039d56baed2da9f89d45bbd673f340ca7898296adc0e9c97'),
 'objects/sha256/e6cd0adac2363d68ae62b2306149f4fafd686f79909ef6f7ab4174b5c911300e': (5134,
                                                                                     'e6cd0adac2363d68ae62b2306149f4fafd686f79909ef6f7ab4174b5c911300e'),
 'objects/sha256/e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174': (95250,
                                                                                     'e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174'),
 'objects/sha256/ecf35c414e8b4bd38d49876b123db3c028b0ff019e5508da5bf8c75ed2011058': (145,
                                                                                     'ecf35c414e8b4bd38d49876b123db3c028b0ff019e5508da5bf8c75ed2011058'),
 'objects/sha256/ed7b95572c47f41f454007eaaa84a6207ef4ec064873869cb99a952352c061d9': (325,
                                                                                     'ed7b95572c47f41f454007eaaa84a6207ef4ec064873869cb99a952352c061d9'),
 'objects/sha256/ef4c7bfb0f716e507fafe900729d2b4ca64b9f0e44cc3b95d059c548307bb951': (2411,
                                                                                     'ef4c7bfb0f716e507fafe900729d2b4ca64b9f0e44cc3b95d059c548307bb951'),
 'objects/sha256/f1df3e1af998d0bbe1487648ffde44d9209561c5d2b9d57eb78f4c39a0be650b': (3896,
                                                                                     'f1df3e1af998d0bbe1487648ffde44d9209561c5d2b9d57eb78f4c39a0be650b'),
 'objects/sha256/f2e71277017b7cf9c169c8a70b79a8cf48f12ec62aca53f1993e3538fd0551dc': (6311,
                                                                                     'f2e71277017b7cf9c169c8a70b79a8cf48f12ec62aca53f1993e3538fd0551dc'),
 'objects/sha256/f38a3b1541522348205a68988905e73607255923c815ddd682c33c4a99d815a1': (2509141,
                                                                                     'f38a3b1541522348205a68988905e73607255923c815ddd682c33c4a99d815a1'),
 'objects/sha256/f3ba0384ba60816f4b8cf3176d8290acd74ff7d8098de88d62770e1d80b5f917': (117632,
                                                                                     'f3ba0384ba60816f4b8cf3176d8290acd74ff7d8098de88d62770e1d80b5f917'),
 'objects/sha256/f3fddd013c20ebe244df3358170a5573c1563abc97dfe05b594750a7696ea096': (5818,
                                                                                     'f3fddd013c20ebe244df3358170a5573c1563abc97dfe05b594750a7696ea096'),
 'objects/sha256/f4acfe05fbd16ae254b120de6fa0198d36419375630c7caff932ec30ead33b18': (10878,
                                                                                     'f4acfe05fbd16ae254b120de6fa0198d36419375630c7caff932ec30ead33b18'),
 'objects/sha256/f600c2928e734f02168620c1f6210b25f685bce079f7eb3051afced14342ac99': (5363,
                                                                                     'f600c2928e734f02168620c1f6210b25f685bce079f7eb3051afced14342ac99'),
 'objects/sha256/f7c22fe056c1e419b367a5822a0ffe79c153decd12ef0d841c4cf6137c82fe3d': (8842,
                                                                                     'f7c22fe056c1e419b367a5822a0ffe79c153decd12ef0d841c4cf6137c82fe3d'),
 'objects/sha256/f8befe641e62c8f58c150223a844b3f08208793e8b8e510bb4012634e67a294a': (15947,
                                                                                     'f8befe641e62c8f58c150223a844b3f08208793e8b8e510bb4012634e67a294a'),
 'objects/sha256/f8d45367f90745a7b7d0e8384d6db083fe9217fa3bca3ef18ab1cee4b03d025c': (888,
                                                                                     'f8d45367f90745a7b7d0e8384d6db083fe9217fa3bca3ef18ab1cee4b03d025c'),
 'objects/sha256/f921da5830bcb3b0c7befb10e05f23346b2ab874c487175217be4a5e752706f7': (149820,
                                                                                     'f921da5830bcb3b0c7befb10e05f23346b2ab874c487175217be4a5e752706f7'),
 'objects/sha256/f9246012815ca3efa1b8a66829b075ded8e650b948fb726cc338ef1ffbbcb2b9': (111418,
                                                                                     'f9246012815ca3efa1b8a66829b075ded8e650b948fb726cc338ef1ffbbcb2b9'),
 'objects/sha256/f9da3f1b170b61193f6d70b21eea8dd90b0782e73f24f1d171a2a24728e9aa77': (2481802,
                                                                                     'f9da3f1b170b61193f6d70b21eea8dd90b0782e73f24f1d171a2a24728e9aa77'),
 'objects/sha256/f9f8db08aeda9ccee02e2c207cc93e10e2a0643ee8125b89e485f1892193aa27': (318046,
                                                                                     'f9f8db08aeda9ccee02e2c207cc93e10e2a0643ee8125b89e485f1892193aa27'),
 'objects/sha256/fa39ca4e94024bf86726af7f73245f92a1b85228ae79831d3d0ea417d1f07437': (380,
                                                                                     'fa39ca4e94024bf86726af7f73245f92a1b85228ae79831d3d0ea417d1f07437'),
 'objects/sha256/fabde3f11c42368f0ffc084b2f35385686a7f1047c17d770c1c57048dbb5b1a9': (13828,
                                                                                     'fabde3f11c42368f0ffc084b2f35385686a7f1047c17d770c1c57048dbb5b1a9'),
 'objects/sha256/fb961048b1434872af6582570b700c000c63f6b8a2510205d03e95fdb3ed78af': (2300,
                                                                                     'fb961048b1434872af6582570b700c000c63f6b8a2510205d03e95fdb3ed78af'),
 'objects/sha256/fc48acbbc407ce88ac99183f286e15fe9029fba4f19480f1e5fe8f532d3ca98b': (6696,
                                                                                     'fc48acbbc407ce88ac99183f286e15fe9029fba4f19480f1e5fe8f532d3ca98b'),
 'objects/sha256/fce3d5e57c62a4d78eb5dee4c73042d0f89aba4422ee3434ed3ccd565b45e490': (118606,
                                                                                     'fce3d5e57c62a4d78eb5dee4c73042d0f89aba4422ee3434ed3ccd565b45e490'),
 'objects/sha256/fd1f67fa7d43a3a7c93adfe3b7703475bbfd8c8c90d50b1aa9526d2ab7cf2150': (7755,
                                                                                     'fd1f67fa7d43a3a7c93adfe3b7703475bbfd8c8c90d50b1aa9526d2ab7cf2150'),
 'objects/sha256/fe413afb55399f4c17b7bd47dfdd5b56ca13560d630ea42036e7557b2c2ba9e3': (28546,
                                                                                     'fe413afb55399f4c17b7bd47dfdd5b56ca13560d630ea42036e7557b2c2ba9e3'),
 'objects/sha256/fefef76dc54d7bb4638b978b17daf66ff470ecc74d18311ec25a72178c15efde': (29754,
                                                                                     'fefef76dc54d7bb4638b978b17daf66ff470ecc74d18311ec25a72178c15efde'),
 'objects/sha256/ff1bca26206753268a3624ac3c214294ff940f50697f4ede66a703030b67f5d5': (113122,
                                                                                     'ff1bca26206753268a3624ac3c214294ff940f50697f4ede66a703030b67f5d5')}
EXPECTED_B_MEMBERS = {'FREEZE_ADDENDUM-v1.md': (2484, '095bf19789550f70b8cd13964e176812a15a8a21145700a69f6b310df37a6fbe'),
 'FROZEN_PAYLOAD_MANIFEST-v1.json': (95250, 'e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174'),
 'README.md': (3168, 'e1e23d17ad510d9cdae30a25f682d995f94964bcac8aadda8081684b42d4c0d0'),
 'RECOVERY_NOTES.md': (4791, '212462b16320ced0cc48428adb10f2351f606c99aa2ced87a788445998d66d8f'),
 'evidence/next-correctness-green-sa20-20261014-packet/after-INPUTS.sha256.log': (94851,
                                                                                  '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-green-sa20-20261014-packet/after-PACKET.sha256.log': (2262,
                                                                                  'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-green-sa20-20261014-packet/after-packet-copy.log': (0,
                                                                                'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-green-sa20-20261014-packet/before-INPUTS.sha256.log': (94851,
                                                                                   '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-green-sa20-20261014-packet/before-PACKET.sha256.log': (2262,
                                                                                   'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-green-sa20-20261014-packet/before-packet-copy.log': (0,
                                                                                 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-green-sa20-20261014-packet/coordinator-driver.py': (2022,
                                                                                '717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f'),
 'evidence/next-correctness-green-sa20-20261014-packet/coordinator-status.json': (623,
                                                                                  '5f40ec078f2239771f09bd9a8704ac6a1375cbaeadbdc031323819307ab33dea'),
 'evidence/next-correctness-green-sa20-20261014-packet/exact-command.sh': (12517,
                                                                           'f5f9de68128cc5f6e142bda7222dbd7ab89c86e9ec769d9d4216dc572ac31712'),
 'evidence/next-correctness-green-sa20-20261014-packet/outer.log': (194915,
                                                                    '92a8eece6c831629f21b948d8b41d020f7f6975102715736a68c903c946c97ff'),
 'evidence/next-correctness-green-sa20-20261014/candidate-corpus-isolation.json': (381,
                                                                                   '70139032edef14a1526c01db4d6c045e5b4c74b8416261b558c116ed0e5f27fa'),
 'evidence/next-correctness-green-sa20-20261014/candidate-corpus/master-s4-compatibility-flush-corpus-v1-sa2.0.51.json': (256,
                                                                                                                          'aa3ccbf61c6be7d640b0929afc02e96ac6de49e7816a5e43c570c9bbc55b703d'),
 'evidence/next-correctness-green-sa20-20261014/coordinator-wrapper-exit.txt': (2,
                                                                                '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'evidence/next-correctness-green-sa20-20261014/external-source-before.json': (3,
                                                                               'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'),
 'evidence/next-correctness-green-sa20-20261014/external-source-stability.json': (55,
                                                                                  '92df286d250ea7db825aae251e94921943b316a9614d0a54be9948591b3daa61'),
 'evidence/next-correctness-green-sa20-20261014/junit.xml': (8084,
                                                             'ce16756d212f6bbde75e2b748b995d3d5dacd0cf62538da3d6fd111969ab98c0'),
 'evidence/next-correctness-green-sa20-20261014/package-origin.log': (290,
                                                                      '1993b871e1dfb8c3393c155a882b355153c0b23594a1a4dacbe2dba43c724103'),
 'evidence/next-correctness-green-sa20-20261014/postgres-start.log': (52,
                                                                      '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-green-sa20-20261014/postgres-stop.log': (56,
                                                                     'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus-manifest.json': (3170,
                                                                              'cab736e3bce08fda1df7e1efa56dac7993ecddb10573dcc72210e4e1779685b1'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                 '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-corpus-v1-sa2.0.51.json': (25700,
                                                                                                      'c8b28c401a3d1753076caecf2c6c65987cfc245ce394c1611bc22274501de38f'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-corpus-v1-sa2.1.3.json': (25665,
                                                                                                     '81a84f72b440ff6969802f995e68a4befaac60451b5d3703bc84aa7edc731473'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                            '94abe1ea69e4cf2eba7e718bdd72a0c5437ba95750158d27c87da189529f4a79'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.54.json': (9210,
                                                                                                            '4312ba346da32cbdf7537e86436500c4f4481b65ee6d4118d02fcda5c9f2d75c'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.1.3.json': (9198,
                                                                                                           '34c7bd12f19310895f86ac03ac6322bbe79ccab5b33fdd32266c420bd07088e1'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                     '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.54.json': (5717,
                                                                                                                     '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                    '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.0.51.json': (831,
                                                                                                                'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.1.3.json': (831,
                                                                                                               'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.0.51.json': (7160,
                                                                                                             '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.1.3.json': (7160,
                                                                                                            '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.0.51.json': (950,
                                                                                                                   '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.1.3.json': (950,
                                                                                                                  '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.0.51.json': (1791,
                                                                                                            '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.1.3.json': (1791,
                                                                                                           '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.0.51.json': (14258,
                                                                                                            '3bd589f9e2a951b888c08dcf72db8196b277922c7b548537262255a2d1498202'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.1.3.json': (14252,
                                                                                                           'd99671ffe7f6dc35a0ee3dce586eaf3337827458ca90a26e787f4ade4430d862'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                           '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                          '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                                      'faec6d27c3fa9223484869f4d7b52687f26ecadc71c78c03b9e4e8ad4b37b859'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.1.3.json': (9210,
                                                                                                                     '72d7cee083de1b7db4ccc02adde96f8b37d10c8474e5fe1aba504166eb18a726'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                               '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa20-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                              '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa20-20261014/progress.jsonl': (45812,
                                                                  'ed43406b9259882aa2978ab8ecf8611dbc573edba0de84e474b6d627a7f2d55b'),
 'evidence/next-correctness-green-sa20-20261014/readiness.log': (46,
                                                                 '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-green-sa20-20261014/runner-receipt.json': (29509,
                                                                       '3a4cc09f74c48f2d1039dbc9626b9fe565c65b87c5c0367d3e22d59696fff368'),
 'evidence/next-correctness-green-sa20-20261014/source-before.json': (16955,
                                                                      '55f42dc25592c28a5d2313d5fcb733836b663491523c7fed5d0d1fa086ee5aea'),
 'evidence/next-correctness-green-sa20-20261014/source-root.json': (183,
                                                                    '2644bc2bb01b255fc4b8c79bf24a090c9e9d5f2fd5ec72aa59d9e19879837019'),
 'evidence/next-correctness-green-sa20-20261014/source-stability.json': (34587,
                                                                         'da522982915ef7c30e4188a315ee726eb270cff482a26f967b320e5ea20eda62'),
 'evidence/next-correctness-green-sa20-20261014/tests.log': (145,
                                                             '3209b3b1ea81a9646875eefbc823dc8770b73ab600c099e4ebc51d1b27b3bf42'),
 'evidence/next-correctness-green-sa21-20261014-packet/after-INPUTS.sha256.log': (94851,
                                                                                  '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-green-sa21-20261014-packet/after-PACKET.sha256.log': (2262,
                                                                                  'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-green-sa21-20261014-packet/after-packet-copy.log': (0,
                                                                                'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-green-sa21-20261014-packet/before-INPUTS.sha256.log': (94851,
                                                                                   '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-green-sa21-20261014-packet/before-PACKET.sha256.log': (2262,
                                                                                   'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-green-sa21-20261014-packet/before-packet-copy.log': (0,
                                                                                 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-green-sa21-20261014-packet/coordinator-driver.py': (2022,
                                                                                '717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f'),
 'evidence/next-correctness-green-sa21-20261014-packet/coordinator-status.json': (623,
                                                                                  '7a5f766120fbc26333a46565504da2e42732add50ae579f6cd40f917dcec0cf4'),
 'evidence/next-correctness-green-sa21-20261014-packet/exact-command.sh': (12517,
                                                                           '4b18107da668c6ca1345fab3ed75cb7711ca91e2ae29f48122c0469fc2819818'),
 'evidence/next-correctness-green-sa21-20261014-packet/outer.log': (194915,
                                                                    '5b5f17855d7b8dac2ad2728322ec46c0c8fc3ab877a2f9ab0d1984892191bc00'),
 'evidence/next-correctness-green-sa21-20261014/candidate-corpus-isolation.json': (380,
                                                                                   '30796cf6c6ed6929ef80408060151b1a26db20f65ec48cc88d2171fcddbaeedc'),
 'evidence/next-correctness-green-sa21-20261014/candidate-corpus/master-s4-compatibility-flush-corpus-v1-sa2.1.3.json': (256,
                                                                                                                         'aa3ccbf61c6be7d640b0929afc02e96ac6de49e7816a5e43c570c9bbc55b703d'),
 'evidence/next-correctness-green-sa21-20261014/coordinator-wrapper-exit.txt': (2,
                                                                                '9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa'),
 'evidence/next-correctness-green-sa21-20261014/external-source-before.json': (3,
                                                                               'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'),
 'evidence/next-correctness-green-sa21-20261014/external-source-stability.json': (55,
                                                                                  '92df286d250ea7db825aae251e94921943b316a9614d0a54be9948591b3daa61'),
 'evidence/next-correctness-green-sa21-20261014/junit.xml': (8084,
                                                             '5c3b2b4df8344725178a7196ba49344cad0e097232b1ae187f935d78c904c0a8'),
 'evidence/next-correctness-green-sa21-20261014/package-origin.log': (290,
                                                                      '1993b871e1dfb8c3393c155a882b355153c0b23594a1a4dacbe2dba43c724103'),
 'evidence/next-correctness-green-sa21-20261014/postgres-start.log': (52,
                                                                      '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-green-sa21-20261014/postgres-stop.log': (56,
                                                                     'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus-manifest.json': (3170,
                                                                              'cab736e3bce08fda1df7e1efa56dac7993ecddb10573dcc72210e4e1779685b1'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                 '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-corpus-v1-sa2.0.51.json': (25700,
                                                                                                      'c8b28c401a3d1753076caecf2c6c65987cfc245ce394c1611bc22274501de38f'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-corpus-v1-sa2.1.3.json': (25665,
                                                                                                     '81a84f72b440ff6969802f995e68a4befaac60451b5d3703bc84aa7edc731473'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                            '94abe1ea69e4cf2eba7e718bdd72a0c5437ba95750158d27c87da189529f4a79'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.54.json': (9210,
                                                                                                            '4312ba346da32cbdf7537e86436500c4f4481b65ee6d4118d02fcda5c9f2d75c'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.1.3.json': (9198,
                                                                                                           '34c7bd12f19310895f86ac03ac6322bbe79ccab5b33fdd32266c420bd07088e1'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                     '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.54.json': (5717,
                                                                                                                     '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                    '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.0.51.json': (831,
                                                                                                                'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.1.3.json': (831,
                                                                                                               'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.0.51.json': (7160,
                                                                                                             '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.1.3.json': (7160,
                                                                                                            '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.0.51.json': (950,
                                                                                                                   '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.1.3.json': (950,
                                                                                                                  '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.0.51.json': (1791,
                                                                                                            '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.1.3.json': (1791,
                                                                                                           '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.0.51.json': (14258,
                                                                                                            '3bd589f9e2a951b888c08dcf72db8196b277922c7b548537262255a2d1498202'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.1.3.json': (14252,
                                                                                                           'd99671ffe7f6dc35a0ee3dce586eaf3337827458ca90a26e787f4ade4430d862'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                           '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                          '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                                      'faec6d27c3fa9223484869f4d7b52687f26ecadc71c78c03b9e4e8ad4b37b859'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.1.3.json': (9210,
                                                                                                                     '72d7cee083de1b7db4ccc02adde96f8b37d10c8474e5fe1aba504166eb18a726'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                               '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa21-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                              '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-green-sa21-20261014/progress.jsonl': (45810,
                                                                  'f34f9390ef44023cb6447cd5227328826cc7f7365a7d1aacc267346e3581878e'),
 'evidence/next-correctness-green-sa21-20261014/readiness.log': (46,
                                                                 '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-green-sa21-20261014/runner-receipt.json': (29508,
                                                                       '585ce3639c165fa390521cee8607e87dea2b831572e191e9d415e6943f955c6d'),
 'evidence/next-correctness-green-sa21-20261014/source-before.json': (16955,
                                                                      '55f42dc25592c28a5d2313d5fcb733836b663491523c7fed5d0d1fa086ee5aea'),
 'evidence/next-correctness-green-sa21-20261014/source-root.json': (183,
                                                                    '2644bc2bb01b255fc4b8c79bf24a090c9e9d5f2fd5ec72aa59d9e19879837019'),
 'evidence/next-correctness-green-sa21-20261014/source-stability.json': (34587,
                                                                         'da522982915ef7c30e4188a315ee726eb270cff482a26f967b320e5ea20eda62'),
 'evidence/next-correctness-green-sa21-20261014/tests.log': (145,
                                                             'dc792aa3ab23850999b9622e5b9a393d4eb476224161d245c3bc7c07d2cbd26a'),
 'evidence/next-correctness-red-sa20-20261014-packet/after-INPUTS.sha256.log': (94851,
                                                                                '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-red-sa20-20261014-packet/after-PACKET.sha256.log': (2262,
                                                                                'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-red-sa20-20261014-packet/after-packet-copy.log': (0,
                                                                              'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-red-sa20-20261014-packet/before-INPUTS.sha256.log': (94851,
                                                                                 '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-red-sa20-20261014-packet/before-PACKET.sha256.log': (2262,
                                                                                 'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-red-sa20-20261014-packet/before-packet-copy.log': (0,
                                                                               'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-red-sa20-20261014-packet/coordinator-driver.py': (2022,
                                                                              '717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f'),
 'evidence/next-correctness-red-sa20-20261014-packet/coordinator-status.json': (619,
                                                                                'a0c0d2349c28286a91c37345446ed6f7853f495f3938c6ab319d823182d4ef2b'),
 'evidence/next-correctness-red-sa20-20261014-packet/exact-command.sh': (7109,
                                                                         '7ce7c6b5552c5ef509876b6b47cf8dd3bd1a225c588b8c0872a46eeea2dbd331'),
 'evidence/next-correctness-red-sa20-20261014-packet/outer.log': (202778,
                                                                  'b8cdb9db5accf774338b84bb3b001227ecc9d4eb5feb87a5d334cd7a305f117b'),
 'evidence/next-correctness-red-sa20-20261014/candidate-corpus-isolation.json': (212,
                                                                                 '5dd2e056467f5d3273c09d3456469b7fb2e21da53960cdbf136a94093311d481'),
 'evidence/next-correctness-red-sa20-20261014/coordinator-wrapper-exit.txt': (2,
                                                                              '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'),
 'evidence/next-correctness-red-sa20-20261014/external-source-before.json': (3,
                                                                             'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'),
 'evidence/next-correctness-red-sa20-20261014/external-source-stability.json': (55,
                                                                                '92df286d250ea7db825aae251e94921943b316a9614d0a54be9948591b3daa61'),
 'evidence/next-correctness-red-sa20-20261014/junit.xml': (24410,
                                                           'ddf480207308914bc864191d6cfbbdace56b8380b7509f332dd5690d5e004de1'),
 'evidence/next-correctness-red-sa20-20261014/package-origin.log': (298,
                                                                    '7ba8a5c83ad7ccf0ba4f4c263c75879e92294b6c023551ff48e5bdeeb1da7d93'),
 'evidence/next-correctness-red-sa20-20261014/postgres-start.log': (52,
                                                                    '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-red-sa20-20261014/postgres-stop.log': (56,
                                                                   'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus-manifest.json': (3170,
                                                                            'cab736e3bce08fda1df7e1efa56dac7993ecddb10573dcc72210e4e1779685b1'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                               '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                              '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-corpus-v1-sa2.0.51.json': (25700,
                                                                                                    'c8b28c401a3d1753076caecf2c6c65987cfc245ce394c1611bc22274501de38f'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-corpus-v1-sa2.1.3.json': (25665,
                                                                                                   '81a84f72b440ff6969802f995e68a4befaac60451b5d3703bc84aa7edc731473'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                          '94abe1ea69e4cf2eba7e718bdd72a0c5437ba95750158d27c87da189529f4a79'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.54.json': (9210,
                                                                                                          '4312ba346da32cbdf7537e86436500c4f4481b65ee6d4118d02fcda5c9f2d75c'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.1.3.json': (9198,
                                                                                                         '34c7bd12f19310895f86ac03ac6322bbe79ccab5b33fdd32266c420bd07088e1'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                   '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.54.json': (5717,
                                                                                                                   '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                  '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.0.51.json': (831,
                                                                                                              'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.1.3.json': (831,
                                                                                                             'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.0.51.json': (7160,
                                                                                                           '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.1.3.json': (7160,
                                                                                                          '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.0.51.json': (950,
                                                                                                                 '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.1.3.json': (950,
                                                                                                                '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.0.51.json': (1791,
                                                                                                          '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.1.3.json': (1791,
                                                                                                         '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.0.51.json': (14258,
                                                                                                          '3bd589f9e2a951b888c08dcf72db8196b277922c7b548537262255a2d1498202'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.1.3.json': (14252,
                                                                                                         'd99671ffe7f6dc35a0ee3dce586eaf3337827458ca90a26e787f4ade4430d862'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                         '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                        '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                                    'faec6d27c3fa9223484869f4d7b52687f26ecadc71c78c03b9e4e8ad4b37b859'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.1.3.json': (9210,
                                                                                                                   '72d7cee083de1b7db4ccc02adde96f8b37d10c8474e5fe1aba504166eb18a726'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                             '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa20-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                            '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa20-20261014/progress.jsonl': (22513,
                                                                '1c160eef8bd87c1cdc67e8620e58afb3f32b4690c1c6dc75efbb9f657c18f01b'),
 'evidence/next-correctness-red-sa20-20261014/readiness.log': (46,
                                                               '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-red-sa20-20261014/runner-receipt.json': (23810,
                                                                     '979a2f1484a0998ca1b1d54287217bd7cc99f6f71726ede098790cd3ac2ae4c4'),
 'evidence/next-correctness-red-sa20-20261014/source-before.json': (16955,
                                                                    'b6012d6e720458563a19fb8cc9337147808d122b941bbd98688ad774fa92e148'),
 'evidence/next-correctness-red-sa20-20261014/source-root.json': (187,
                                                                  '7b9d408e75e3c14a86661c7b8650b9f0520b002a5425ea9528d529b6dd203e8a'),
 'evidence/next-correctness-red-sa20-20261014/source-stability.json': (34587,
                                                                       '38d864add1d8e41fb57add6eb4cc772bbdb96fb29845be282225760f52c1ef21'),
 'evidence/next-correctness-red-sa20-20261014/tests.log': (18755,
                                                           '584c083c9482a3ab51ba2c06e465212b9b8d3d67daf914b10a67189b64e52fda'),
 'evidence/next-correctness-red-sa21-20261014-packet/after-INPUTS.sha256.log': (94851,
                                                                                '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-red-sa21-20261014-packet/after-PACKET.sha256.log': (2262,
                                                                                'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-red-sa21-20261014-packet/after-packet-copy.log': (0,
                                                                              'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-red-sa21-20261014-packet/before-INPUTS.sha256.log': (94851,
                                                                                 '65c92526f3bc9ac8657cf4696e4ca4107a11604b30ab77939cbb09966557f232'),
 'evidence/next-correctness-red-sa21-20261014-packet/before-PACKET.sha256.log': (2262,
                                                                                 'aac2c7680d0af4840ba7c29d3c2073f218f6aeac6a06f56c67a47b345c93297b'),
 'evidence/next-correctness-red-sa21-20261014-packet/before-packet-copy.log': (0,
                                                                               'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
 'evidence/next-correctness-red-sa21-20261014-packet/coordinator-status.json': (307,
                                                                                '08da2b5b3276490731ac1708960ab160a63d9fa98b1dd460b530a81ed5026270'),
 'evidence/next-correctness-red-sa21-20261014-packet/exact-command.sh': (7109,
                                                                         '8e9d48e071ac8d3de5cfe2ac61f615c5c4b11df5f45b1373db0bcbd6561ca9f9'),
 'evidence/next-correctness-red-sa21-20261014-packet/outer.log': (202778,
                                                                  '1b14cafe8d0e732804296a9ac5cc4cc202315dea718bd8c18466217e246a0eae'),
 'evidence/next-correctness-red-sa21-20261014/candidate-corpus-isolation.json': (212,
                                                                                 '5dd2e056467f5d3273c09d3456469b7fb2e21da53960cdbf136a94093311d481'),
 'evidence/next-correctness-red-sa21-20261014/coordinator-wrapper-exit.txt': (2,
                                                                              '4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865'),
 'evidence/next-correctness-red-sa21-20261014/external-source-before.json': (3,
                                                                             'ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356'),
 'evidence/next-correctness-red-sa21-20261014/external-source-stability.json': (55,
                                                                                '92df286d250ea7db825aae251e94921943b316a9614d0a54be9948591b3daa61'),
 'evidence/next-correctness-red-sa21-20261014/junit.xml': (24410,
                                                           'dc2f42ac693296d353a2ab525e1e0b24e1c17b87322377574a2c85ca21cf9be0'),
 'evidence/next-correctness-red-sa21-20261014/package-origin.log': (298,
                                                                    '7ba8a5c83ad7ccf0ba4f4c263c75879e92294b6c023551ff48e5bdeeb1da7d93'),
 'evidence/next-correctness-red-sa21-20261014/postgres-start.log': (52,
                                                                    '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-red-sa21-20261014/postgres-stop.log': (56,
                                                                   'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus-manifest.json': (3170,
                                                                            'cab736e3bce08fda1df7e1efa56dac7993ecddb10573dcc72210e4e1779685b1'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                               '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                              '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-corpus-v1-sa2.0.51.json': (25700,
                                                                                                    'c8b28c401a3d1753076caecf2c6c65987cfc245ce394c1611bc22274501de38f'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-corpus-v1-sa2.1.3.json': (25665,
                                                                                                   '81a84f72b440ff6969802f995e68a4befaac60451b5d3703bc84aa7edc731473'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                          '94abe1ea69e4cf2eba7e718bdd72a0c5437ba95750158d27c87da189529f4a79'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.0.54.json': (9210,
                                                                                                          '4312ba346da32cbdf7537e86436500c4f4481b65ee6d4118d02fcda5c9f2d75c'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-flush-corpus-v1-sa2.1.3.json': (9198,
                                                                                                         '34c7bd12f19310895f86ac03ac6322bbe79ccab5b33fdd32266c420bd07088e1'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                   '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.0.54.json': (5717,
                                                                                                                   '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                  '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.0.51.json': (831,
                                                                                                              'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-lifecycle-corpus-v1-sa2.1.3.json': (831,
                                                                                                             'fe740c44e9db87450be5a48a45d77d1fdcebcae035ce70a57c3e25ed6a8821d7'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.0.51.json': (7160,
                                                                                                           '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-method-corpus-v1-sa2.1.3.json': (7160,
                                                                                                          '6bffab1728d2f6db5199a5b65870c43ee1ffed3e7ab4af4dca36ad6f61f2a6df'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.0.51.json': (950,
                                                                                                                 '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-relationship-corpus-v1-sa2.1.3.json': (950,
                                                                                                                '9d3ec65a3832e673c250854ebd7305f72ab4e55b8f043114a1a9af9124a58af1'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.0.51.json': (1791,
                                                                                                          '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-state-corpus-v1-sa2.1.3.json': (1791,
                                                                                                         '6d9f2dc3b3adb25eff3afb8d4f2f55cbc2cf30b000c9d95e42290505f33fd3b8'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.0.51.json': (14258,
                                                                                                          '3bd589f9e2a951b888c08dcf72db8196b277922c7b548537262255a2d1498202'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/compatibility-truth-corpus-v1-sa2.1.3.json': (14252,
                                                                                                         'd99671ffe7f6dc35a0ee3dce586eaf3337827458ca90a26e787f4ade4430d862'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.0.51.json': (9156,
                                                                                                                         '3c7b25b38f10b7449e2d839ec55407757fdb74ca95702082f4f2ee013c28af88'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-core-flush-corpus-v1-sa2.1.3.json': (8748,
                                                                                                                        '5c93e7b3677a006340bf010f7bc2c44e5ffd3d973608aa6638770cbe77d1d6cb'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.0.51.json': (9210,
                                                                                                                    'faec6d27c3fa9223484869f4d7b52687f26ecadc71c78c03b9e4e8ad4b37b859'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-flush-corpus-v1-sa2.1.3.json': (9210,
                                                                                                                   '72d7cee083de1b7db4ccc02adde96f8b37d10c8474e5fe1aba504166eb18a726'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.0.51.json': (5717,
                                                                                                                             '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa21-20261014/prior-corpus/master-s4-compatibility-implicit-flush-corpus-v1-sa2.1.3.json': (5717,
                                                                                                                            '2df702b1633e96f8ae8510bab2305cd8dcd017c7a8926385d343412156e86c16'),
 'evidence/next-correctness-red-sa21-20261014/progress.jsonl': (22516,
                                                                'a2d085a7deee0e1b77debedd6a0096d3973655563c2601ea00cdcb74c527022d'),
 'evidence/next-correctness-red-sa21-20261014/readiness.log': (46,
                                                               '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-red-sa21-20261014/runner-receipt.json': (23809,
                                                                     '441f0679bfe28c96152d5167652128ec4734b5e4f381c51e8d0f4f800c994c44'),
 'evidence/next-correctness-red-sa21-20261014/source-before.json': (16955,
                                                                    'b6012d6e720458563a19fb8cc9337147808d122b941bbd98688ad774fa92e148'),
 'evidence/next-correctness-red-sa21-20261014/source-root.json': (187,
                                                                  '7b9d408e75e3c14a86661c7b8650b9f0520b002a5425ea9528d529b6dd203e8a'),
 'evidence/next-correctness-red-sa21-20261014/source-stability.json': (34587,
                                                                       '38d864add1d8e41fb57add6eb4cc772bbdb96fb29845be282225760f52c1ef21'),
 'evidence/next-correctness-red-sa21-20261014/tests.log': (18755,
                                                           '7e34bb558a8e69ab09105feb66af00154b02eb9715a0de8f8cf88b6804d81a62'),
 'experiments/next-unblocked-correctness-20261014/BASELINE_SOURCE_MANIFEST.json': (24182,
                                                                                   '3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703'),
 'experiments/next-unblocked-correctness-20261014/BASELINE_sqlalchemy.py': (63625,
                                                                            'df8ee448ed7bab52e5e1ecd61f5cd859464d4607fbac13b3ac62c2def4a5ece9'),
 'experiments/next-unblocked-correctness-20261014/FINDING.md': (4329,
                                                                '6fa7b4532ef1bd1466976177b4124eca0efef578541fcaca808f06582372b538'),
 'experiments/next-unblocked-correctness-20261014/GREEN_SOURCE_MANIFEST.json': (24315,
                                                                                '4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649'),
 'experiments/next-unblocked-correctness-20261014/INPUTS.sha256': (136515,
                                                                   'e52d6deaba016ff135f608ce50dde875adc82bedc109471350022a660050091c'),
 'experiments/next-unblocked-correctness-20261014/NATIVE_SOURCE_PINS.sha256': (3012,
                                                                               '9cc74cbd6ab6cd9e174c6eaa8763c307341c9d18322b40697af62778542a7b64'),
 'experiments/next-unblocked-correctness-20261014/NEW_NODE_IDS.txt': (3019,
                                                                      '94cc5449cb1ca3e0b1c87ec1f38196c027f4c6505b19bd7fe21efc539ffea3da'),
 'experiments/next-unblocked-correctness-20261014/PACKET.sha256': (3378,
                                                                   '6fcf4c01a281746d6e665e750462dc706bfed31f01ef855a97330540164bec7a'),
 'experiments/next-unblocked-correctness-20261014/PLAN.md': (4866,
                                                             'eee951b1b7a5033e7b4d5c607afb6001fafe944c80ca29025af98782c67d9fcb'),
 'experiments/next-unblocked-correctness-20261014/PREPARATION_CHECKS.json': (886,
                                                                             '1d3657f6be42e00f55ac104a3daa83b43ac3d13a69c1b577067f4e96e8a7c15a'),
 'experiments/next-unblocked-correctness-20261014/PREPARATION_INCIDENTS.md': (1801,
                                                                              '22cef8c7c1ada24a751f2e77a5f1203864c7183dacd1e48ce2f16f05c6886576'),
 'experiments/next-unblocked-correctness-20261014/RED_SOURCE_MANIFEST.json': (24319,
                                                                              '592a2a0e4f386e8da188e10c3a5d530e675e16c6ec30d78505b66a27fd7a4c3d'),
 'experiments/next-unblocked-correctness-20261014/REGRESSION_NODE_IDS.txt': (2976,
                                                                             'fc24931e2699a07101b7a611a1e2a1175a2d707c5399ba5c267b220c3ad25d23'),
 'experiments/next-unblocked-correctness-20261014/ROOT_COMMANDS.txt': (39459,
                                                                       'c474618b435dbf3de5ca2d96cd0338d3602f0c8f66b3dafeb840b9a11e28dd3e'),
 'experiments/next-unblocked-correctness-20261014/ROUTE_COMPARISON.md': (1930,
                                                                         '1f7e118cc0520cc8384279dbe6d4b86db87b0c61e4f91a0d8c0c73dfd9815a85'),
 'experiments/next-unblocked-correctness-20261014/SOURCE_DELTA.patch': (20409,
                                                                        '09cf92230de139199d6fb01b9b52d747302a653ed7edff203703f325d6967cbd'),
 'experiments/next-unblocked-correctness-20261014/baseline-source.sha256': (21969,
                                                                            '741e1f91a460fba027b6564432946842da75c04cd8a394a7b2b5ac154388fbae'),
 'experiments/next-unblocked-correctness-20261014/green-source.sha256': (22086,
                                                                         'e77144847a3ba00c94952fa26e4d1d508e217aed3ee3db6b750006138b114f63'),
 'experiments/next-unblocked-correctness-20261014/red-source.sha256': (22086,
                                                                       '59416d927951d238297fab58c2e686a4a36e9b31ce40dc6de5275cafb8b76a96'),
 'freeze/FREEZE_AUTHORIZATION-v1.json': (817, '0a06445055a51bbd45f69756e03c96f2f89225fa2d3da52b419ab7ee4b3b0059'),
 'freeze/FREEZE_CONTROL_ALLOWLIST-v1.json': (42199, '8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176'),
 'freeze/FREEZE_CONTROL_INVENTORY-v1.json': (7271, '12fddef4f7cb00520d88fcbb7909f756714aaf085e293aee62f6952a0835b69a'),
 'freeze/FREEZE_SENSITIVE_SCAN-v1.json': (1042, '64c4d315ea0b0918f529248faab75e261dce6445583dabfa7e574c81cba9c310'),
 'freeze/ORIGINAL_RECHECK-v1.json': (2184, 'a7944ca7e406de3df3ccc4db30a2dd7faf86f3bfb44dafe944d6e34244fcbfb1'),
 'freeze/freeze_capsule.py': (19399, 'b1b17b973820a440b4ef43c3535712d97227f3f53a8c94ab4f1252fc357e7592'),
 'freeze/independent-review/REVIEW_ARTIFACTS.sha256': (789,
                                                       '086bc51c5c374575be2d02ae0583bdf08e90a35e2239e43039509c6bcb86e3a5'),
 'freeze/independent-review/VALIDATED_INPUTS.json': (111996,
                                                     '1f6e334bf6531c1004518f1171ce70fdb1836bc93f4e90588f51967ca92c25fb'),
 'freeze/independent-review/audit-summary.json': (4075,
                                                  '7641e39d5bf45f9b1fd57eaf466b846e7dc0c0c52349fd2d03b9f74e6bf5485f'),
 'freeze/independent-review/audit_inputs.py': (22371,
                                               '0d40992126616a03626ac36954554f1d246f9322ce5a2afed1960c41f8c9790c'),
 'freeze/independent-review/checked-inputs.json': (167541,
                                                   'e13d3f4c3825a99f3b026d5433ca08ab460c8c972cc5700b9444802b223dbc8a'),
 'freeze/independent-review/filename-validation.json': (830,
                                                        '86807914a89a2f4eff4e291bff314faa933bb68ee18a7cc15525e9d342bd6374'),
 'freeze/independent-review/node-reconciliation.json': (23653,
                                                        'cc2cf376d831364674d26c539646955a4f1c3a3c86549449d878722eb06e219d'),
 'freeze/independent-review/review.md': (5412, '5e8b065421a1f50c185f8c00f9f5be40070acacbfa8e05798cd43dc8f9bf5e63'),
 'freeze/independent-review/secret-pattern-dispositions.json': (1079,
                                                                '640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022'),
 'freeze/independent-review/secret-pattern-scan.json': (689,
                                                        'c6b662e5b139bd591720783a3b8194679c6ca0edc9069f6aa150a4099b00e14b'),
 'freeze/independent_rebuild_restore.py': (13774, 'd4c17c7662c220434c889f8b8d3c38c60f1f57a7809ffaad9c44a628b841fe03'),
 'freeze/preparation/ALLOWLIST_SUMMARY.json': (585, '3996cc376bc83b6e928f7866625f247e37fbc29138bdf05076a2b2095fc54f5f'),
 'freeze/preparation/COPY_ALLOWLIST.json': (117133, '442857ea6560e7600566eee05823f968d58e9c2df0feccb98f05af82e3dce173'),
 'freeze/preparation/COPY_RESULT.json': (432, '3abfd4801f10f094b1843665c2bc61286ff821218988e2699960a968bf01f0d1'),
 'freeze/preparation/EXCLUDED_CACHE_DIRECTORIES.txt': (131,
                                                       'd61ec4bcca47dcfcf6ac25ffee4bca7c247c7fc3e4b1141f041927af49f94dd2'),
 'freeze/preparation/GENERATED_FILES.json': (657, '032b08923134a6fe9d4567446db78d156333faeab0fa197bd4fdee9bf5b1d9ef'),
 'freeze/preparation/PREPARATION_REVIEW.md': (3462, 'a30588daa563ef72987b0d017c14d64a68b1766574368d15ee4635e66279a189'),
 'freeze/preparation/PREPARED_CANDIDATE.sha256': (63968,
                                                  'aaec85c083fa001754b488dd89196db5d303c7b464f80eb13a4cd9f5ab344a6e'),
 'freeze/preparation/PREPARED_INPUTS.json': (167605,
                                             'aadaf38be9c80103fbdf90f736491fbe928a1acb918180c1d2100a0f3aacafc7'),
 'freeze/preparation/PREPARED_PAYLOAD.sha256': (63808,
                                                'e9486b5a85f2b7e287bd57791c53901fded78eed35f0dd2b241587112fbd8aae'),
 'freeze/preparation/PREPARER_DATA_CHECKS.json': (3597,
                                                  'f612589c82d8ed64e125988659d456830c66874a41f5eab540a2c3091d75ea23'),
 'freeze/preparation/SOURCE_FILENAME_ALLOWLIST.txt': (7764,
                                                      'a20f6dffc27545837d8399f390263057141df5690dc84ebf219367747ff17148'),
 'freeze/preparation/prepare_snapshot.py': (12921, 'd74915967fdafed2483a7c656bb503fdc5c5353ed26ecabc91a8f4183e8fb0da'),
 'freeze/preparation/verify_prepared.py': (9320, 'cdd39cc5be8121d1ae6b0dc4637d4eb29fcd0655c9f982cf5da16ac70ec0701a'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/audit-checks.txt': (1910,
                                                                                   '7c732571d81b4e74ceef24c0bb104e4fa962b23fa16e3419f8ee3a98ae06d1df'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/audit-summary.json': (3053,
                                                                                     'aa936b86b92c332954eda5c479f915e3968617af043ba939d942c6bf169f67ad'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/audit_evidence.py': (21300,
                                                                                    'b457d4f4d6a718810b0f43feb453914bb2af5b1b807b31e99d05a1817ea164c7'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/node-audit.json': (13616,
                                                                                  'a8614b838c30b9666bc5ba4f10d6088694969425435ab5a082a0dd29aaf9b6ba'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/pin-name-validation.txt': (256,
                                                                                          'b5687c112bb6570e3be2440f605806557dae9ae92fb48acf3254564db5e60a1c'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/review.md': (15012,
                                                                            'b2e56c9a65989b62b4076febfa56b3041167ab87f0a107cdc0de54e8b9bd9d88'),
 'reviewer-notes/async-cleanup-green-sa20-independent-20261014/sa21-comparison.json': (262,
                                                                                       '5f0462911a4bf39b22c8853d597277d7aeffcb89ebece02677c40ecdfaaf48e1'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/audit-checks.txt': (1738,
                                                                                   '2951b2801905f4efd8cdaddf94aab5d8b83539ec69690024ac561e9f8e7cb253'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/audit-summary.json': (2873,
                                                                                     'ed7bdcceeebb06bfc38116c55eef6ae8f6854e2fdf5d7e141e08722596c740d5'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/audit_evidence.py': (18541,
                                                                                    '60d1d2da05688d6faf0ea5068d4861652fc93bfba9b2906252ad18a9d8c047f6'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/node-audit.json': (13616,
                                                                                  '703d767d698059b36ea170cb3bf85dd62ab407e5372b3451932218e5c8a4075e'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/pin-name-validation.txt': (256,
                                                                                          'b5687c112bb6570e3be2440f605806557dae9ae92fb48acf3254564db5e60a1c'),
 'reviewer-notes/async-cleanup-green-sa21-independent-20261014/review.md': (14182,
                                                                            'd241277d4b7899f43f48cc26daee884745732b66d53591b74b22174e521c0c49'),
 'reviewer-notes/async-cleanup-primary-contract-20261014/contract-review.md': (14057,
                                                                               '385d31a6e50daf0bcd3ce4d13026f36f749c2bd488618c66522025b83111f491'),
 'reviewer-notes/async-cleanup-red-plan-independent-20261014/frozen-identities.txt': (408,
                                                                                      '504c1b71c18b20f728c9a24a22d68a9fa9fc94b8f049df45b95a1dca3555efdd'),
 'reviewer-notes/async-cleanup-red-plan-independent-20261014/review.md': (10052,
                                                                          '00e1e543eb3684838e2610517d50001516c0ad488e9272d462f372b20804c278'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/audit-checks.txt': (1996,
                                                                                 'b9c87b8e29fcda8afdf322d17b59c09f9ac5228054b1b067911913d772af2787'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/audit-summary.json': (3110,
                                                                                   'c3fba550c6e9113e1c6e20888adbcb6ab48f8779de94171d16c518e42be3a980'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/audit_evidence.py': (20228,
                                                                                  '5245cd63d6ecc8faaa6671ca3d723b69f6447c420cc9607125d356d1aac3c844'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/node-audit.json': (6056,
                                                                                'a3ae3ba6e36a156caae7fcf68305f8fe0c4e5924d35fadc599a653b7d1b7dda2'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/pin-name-validation.txt': (256,
                                                                                        'b5687c112bb6570e3be2440f605806557dae9ae92fb48acf3254564db5e60a1c'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/review.md': (18288,
                                                                          'e74431dbae567b71617d6da732fa846fe389afe763a7ceb3206fcf44ca8f9701'),
 'reviewer-notes/async-cleanup-red-sa20-independent-20261014/sa21-comparison.json': (7647,
                                                                                     'a5d69aa552d6da4c18d5364a2c5114e98d448b5c0f5e2a7c71695f396277be94'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/audit-checks.txt': (1553,
                                                                                 '385cd456838b530bc2623ae42dd00f7d292cdbbb4acaa2e249a1de5c729a34d8'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/audit-summary.json': (2198,
                                                                                   '5e1bb462587fde28603ba0aa297eec9d5b6179ecd53860440228c275406a5480'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/audit_evidence.py': (13455,
                                                                                  'd5ebc9b0adbe777739a49c0f1ace0c7e9220fb7e50034d664a7e2e214d31d17f'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/node-audit.json': (6056,
                                                                                'a3ae3ba6e36a156caae7fcf68305f8fe0c4e5924d35fadc599a653b7d1b7dda2'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/pin-name-validation.txt': (256,
                                                                                        'b5687c112bb6570e3be2440f605806557dae9ae92fb48acf3254564db5e60a1c'),
 'reviewer-notes/async-cleanup-red-sa21-independent-20261014/review.md': (10983,
                                                                          '1eca8aa2d3dff9f31694d86ccf76773d92ecff108f3b54a4db00fecafc2b5683'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/green-sa20-reviewed-command.sh': (12517,
                                                                                                         'f5f9de68128cc5f6e142bda7222dbd7ab89c86e9ec769d9d4216dc572ac31712'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/green-sa21-reviewed-command.sh': (12517,
                                                                                                         '4b18107da668c6ca1345fab3ed75cb7711ca91e2ae29f48122c0469fc2819818'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/red-sa20-reviewed-command.sh': (7109,
                                                                                                       '7ce7c6b5552c5ef509876b6b47cf8dd3bd1a225c588b8c0872a46eeea2dbd331'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/red-sa21-reviewed-command.sh': (7109,
                                                                                                       '8e9d48e071ac8d3de5cfe2ac61f615c5c4b11df5f45b1373db0bcbd6561ca9f9'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/review.md': (15208,
                                                                                    '03fda830de5d4bfebeb57bee95358f9cb0513e019adfa06dab50bd4918563ce4'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/reviewed-coordinator-driver.py': (2022,
                                                                                                         '717e037b8a6011f68c599d3dbab23a7d65e7c5e6f7c09b79d3ba15b7aa0b3f8f'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/shell-syntax-check.txt': (436,
                                                                                                 '2cf960b47114f7a297243408ec3830e242591a1246f517e8b456111cf1def8ce'),
 'reviewer-notes/async-cleanup-remaining-commands-independent-20261014/static-check-summary.txt': (1720,
                                                                                                   '7719949d600e4c0f59cdca872326349cede64c3eda93e3a62860596337b00b2e'),
 'source/AGENTS.md': (6154, '38987c61d5d6f65aa4aeb59148e27c238f37c08e121a5ef5dd8e543736e43c01'),
 'source/ENGINEERING_PLAYBOOK.md': (10762, 'bc6a11657681d9f19364205b1d4a77230763696bff35010e211edd38e99812df'),
 'source/LICENSE': (1070, '7f5a6a6ca9e6e2d6e75ec8530612396f3eebd2659c79a6ca123bf30a933f23df'),
 'source/README.md': (13377, 'a0fbe0cbc8646d8c00eeaebac27fde419047cb420473759b4194ee5d3c925595'),
 'source/docs/_reset/notes.md': (12735, '722fffb69f4daa8a3ebf0eb15b487cd463f84e13e7c3d28b6ccd4594365e831f'),
 'source/docs/architecture/README.md': (23002, '20623faaa261e9c071f2a2d014d6b37cdef245c2d46c5a953ac509bf0f7a0c59'),
 'source/docs/build-guide.md': (11951, 'b0babeadc6c05d70a31a15837a183af19a61d3a839c04724536b1be9f79a2804'),
 'source/docs/compatibility.md': (26001, 'aeba6decd4f8030b999538c2d3871440e00f9b0f623cb764970cdec2fb242176'),
 'source/docs/decisions.md': (11234, '7f61ecb62f61ff064f4490e78805444ef5d17c57164df9733b4b33b1b0c8091d'),
 'source/docs/doctor.md': (12846, '722c650fda4da8bf27c1d27a751a88f363da314293aadd40b969b7ececd06c2e'),
 'source/docs/lifecycle.md': (22678, '093bfc35266da35ad343210bb09bf97e8cea47e27e1843317d913eb01fbe8b8f'),
 'source/docs/prior-art.md': (12794, '9979715af3c74c0e5abb99dd413f7a9269af503f432cabee25b9305096824293'),
 'source/docs/research/CRYPTALIS_FINAL_REVAMP_BLUEPRINT.md': (1746649,
                                                              'ceb2fa7376b169dff636e678977139b7b1dd9f63c2c45e0d7ec98a22d261228e'),
 'source/docs/research/CURRENT_COMPATIBILITY_CORPUS_20261012.json': (222039,
                                                                     '9df455d63a89a0cb1cc4e6ee22bfdd0e3b50c2899187265bf3a8081bccebe971'),
 'source/docs/research/CURRENT_VERIFIED_CHECKPOINT.md': (18743,
                                                         'e3e981b4f524a463b33468be59bce153608b843bad2e72d4f13bab79198702a7'),
 'source/docs/research/DEFECT_REGISTER_20261012.md': (25765,
                                                      'ab13363966b0f5979747e435c77cdc8f8ecfc6d630062155a2bd2b3a4441b0ba'),
 'source/docs/research/DELETE_TEMPORAL_CHECKPOINT_20261012.md': (2762,
                                                                 '578bfbceb86a25318021e464d28e16f026f50ab3a1cacdd1103ae8435f57dc0b'),
 'source/docs/research/DX_ENGINE_PREFLIGHT_20261013.md': (3400,
                                                          '913a9b42b39646f80c0c55f37b47c57f323d988a75a94f065f45d6ce7a7259c3'),
 'source/docs/research/INPLACE_LAYOUT_RESEARCH_20261012.md': (3948,
                                                              '89c1488ab138dee26dc0d0f119d3702324caf3df9d1522428cc240c3653c5617'),
 'source/docs/research/LAYOUT_COST_AND_COMPETING_DESIGNS_20261012.md': (4792,
                                                                        'ae082e67192f7474a6d31c05ad3db235a31f21b1ea1c22e2b1d1a0b4241f9bdf'),
 'source/docs/research/MANIFEST_SETUP_20261013.md': (6925,
                                                     '1dca76e91c8fb5bf3a152ec56cda558a92276a58ad96366b3ba3a2398c96a118'),
 'source/docs/research/NATIVE_DELETE_CHECKPOINT_20261012.md': (2462,
                                                               '148884ffd9f2eaf129b87c2187f7f1d41b09e851c6cb3e785b4a291d1a89f9c6'),
 'source/docs/research/NOT_INCLUDED_20261012.md': (560,
                                                   'bbb01253517840afc087ed2494e3186865af2fa1a725392cdf9b9d28f766aeac'),
 'source/docs/research/PRIVATE_PUBLIC_UPDATE_20261013.md': (10090,
                                                            'a182472b08d9bf696079a052773455df1010a6ec9cd47ce629812c2cda8c52a3'),
 'source/docs/research/README.md': (1228, 'f47b5570ecd76c324f01d7805d813381dbc3b05a2243c4bd8845222f67678cd6'),
 'source/docs/research/RESEARCH_CANDIDATES.md': (1757,
                                                 '898819b846380bf148ea8e739f605b28ea9d958b51434ba1259e75b37153f5c4'),
 'source/docs/research/SEARCHABLE_REVERSIBLE_CHECKPOINT_20261012.md': (5765,
                                                                       '460b6f0b0e3e4aed058b3ec5e763ec21f96b5c0b644b6350a6794fac5e2a0e8b'),
 'source/docs/research/TEXTUAL_REFERENCE_REFUSAL_CHECKPOINT_20261013.md': (4530,
                                                                           'a2d489e8f00b904a0560ae329b7225de8dd7cd9566905d472253d69d1b72f0e3'),
 'source/docs/research/council-review-1/report.md': (17846,
                                                     'dace62c1a3036095a14570b2e0430901aa28b8300eaa135e4b90f2d475b6a641'),
 'source/docs/research/council-review-2/report.md': (5403,
                                                     '3dbe2be24e18cdbb5f97f5e88568f791daa5e10a9171089a23121b592e7479f2'),
 'source/docs/research/council-review-2/work-ledger.md': (7206,
                                                          '09c8b885fa6c6e3426205f2bb176b417168c0908aae08d547c89fd7e3b4dde4c'),
 'source/docs/research/cryptographer-review-packet.md': (42514,
                                                         '8f9a21f08082ce595fe75c648ed91aa5ddd8ad306893a44cf5dd7758da2e8f73'),
 'source/docs/research/hardening-evidence.md': (6809,
                                                'e9d163caa8ced42c75893f59815a2a30b823f00c8525b6fa2ccfc2794b540733'),
 'source/docs/research/hardening-resolution.md': (17131,
                                                  '27b5e3d554f99596defb29e9fbc40858e74f0429d14d6964a8161cdbbda24fba'),
 'source/docs/research/performance-checkpoint.md': (18200,
                                                    'bd55fcd474ff411a8708510fe260c174bc2a1c9d5381bd17f24d836fed43f0bd'),
 'source/docs/research/reset-crypto-authority-evidence.md': (22505,
                                                             '3413219dfd2e3e439fb4cbc2d25e6585f853f3c3d3463370e0020f713cb5a772'),
 'source/docs/research/reset-integration-search-evidence.md': (36262,
                                                               '5f7a3f44c28e3401eaa652c1edd6a05bd86f726e10f81b6eddca2a936eff9d90'),
 'source/docs/research/reset-leakage-semantics-evidence.md': (8554,
                                                              '44519fde2adbc643562e58ac7b58784e904e57dca8507f34ce72b922beb5b54c'),
 'source/docs/research/reset-operations-release-evidence.md': (24436,
                                                               'b888bb61657044ac8ff7a91740c09c6a26c6317a78a1683506ec56843747c4ca'),
 'source/docs/research/reset-traceability.md': (131467,
                                                '07905f69e676e1bed111375d474b1c5d8e5e72f8831bad986bcf8586b9b6e823'),
 'source/docs/research/revamp-evidence.md': (48163, '815761e3cca9d18aef254bd25d543d381f51fc54e18258c1e7a0f21914811c73'),
 'source/docs/security.md': (31672, '27546dd4022c4a3353066bec05dee76e97cda8a4f1e16e26b656e7572b0abc45'),
 'source/docs/status.md': (68283, '31d35e60db1de7ab2a6939d0c061118e6cee9000f0705c943209ca7086fcddbb'),
 'source/docs/walkthrough-migration.md': (4330, '31fe61df71acfaefd8570b1438ea0a5a13a1805dc8f88c8bc5aca3b97db964d0'),
 'source/docs/walkthrough-search.md': (2882, 'f2bfebbd07c80b511207b1d746136fde05224a0f8cc9239018d296c8efc5af05'),
 'source/docs/walkthrough-sqlalchemy.md': (2911, 'de07d118889fa01b674aec8cb909e69da7f1edb2c77be577da2f4f1bd5ca96d3'),
 'source/examples/active-state/genesis.json': (395, 'f4a1e408b6303cb9dc4cb094770d49346609790a0ee5e00337e1b5afe8b14763'),
 'source/examples/active-state/successor.json': (491,
                                                 'aea1f6f6b022d390f9a8fc68cad482d7c4df47b14e602076d354b7834f4635ab'),
 'source/examples/demo_manifest_history.py': (4344, 'bad9d66bbb99ab788286ccbe10f4215d3c1eec73d6f4124d8c1d2672ad5df628'),
 'source/examples/demo_smolink_crypto.py': (12461, '9197d05f04937e14ce317245c97aa9d5d7e3777c4c13a49b01bb621ca114a4a6'),
 'source/examples/envelopes/f1-structural.hex': (291,
                                                 '60effcfdfced026cadf09afa94ee7d300f178693b61136adfa9186019a6c8bb9'),
 'source/examples/envelopes/w1-structural.hex': (319,
                                                 'd7eda7903401ce52bc67cbc01c3bd3bd02ac05b78d1ffaef66743c4eb04440c9'),
 'source/examples/field-formats/parameterless.json': (454,
                                                      'f5a0a56b8b7332a99fcff8a48314fff3241592c1f521b2c6681653326e2c13b1'),
 'source/examples/manifests/genesis.json': (125, 'ab9fb3baa09924c883940c926b2406c3e6604e93b95eb1cc024cc89f51fa24a2'),
 'source/examples/manifests/invalid-duplicate.json': (184,
                                                      '6e82f332c08ad8ad1ab8355c190c77210ec94e15b27d21b5b1029cbff4e4b970'),
 'source/examples/manifests/invalid-successor.json': (167,
                                                      '7facec7579d006cbd50f71e42a24675c1640685ac03e0d5f159f45da497771d6'),
 'source/examples/manifests/successor.json': (187, '2e9881b401babc7238764df0ac5ee108b4e14c0d9935727ca419b5edcfd821bd'),
 'source/examples/scalars/candidate-vectors.json': (1003,
                                                    '8028c66f120118c3bf0de9f93aeeca23da5c5893624b44c5a16a52e74ca33be9'),
 'source/experiments/manifest_setup_fastapi_models.py': (5788,
                                                         '220f4640722c520948afd7db4179f8c4c815eb51da4ae71cca73a4a0d7fa51aa'),
 'source/pyproject.toml': (552, '4653756dfe6a3dd1a185f636efb1ea0135b5235d9cdc138f30667d1f0975487f'),
 'source/scripts/test_postgres.py': (6071, '118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12'),
 'source/src/cryptalis/__init__.py': (36, 'c1a82f9f958187e4b5423d11df5a035b17d75b34a0947af6be4aac436cd2fed2'),
 'source/src/cryptalis/__main__.py': (58, '9967032819ce6f18e02a40d033958d5f4f7c328faf8693bc07ecc42a1a525707'),
 'source/src/cryptalis/_doctor_ciphertext.py': (4359,
                                                '42e9424fbe55e982463032668a9365bed2c796714ff17649da2adf725fa6e755'),
 'source/src/cryptalis/_doctor_setup.py': (10364, '6637ff4aee2b4ac27628d56ea9b73ad5e2380782eebc0bba23192c3eff1583e6'),
 'source/src/cryptalis/_experimental_public_delete.py': (18468,
                                                         '074c0e41cd728ec5e59bb20665b22bc2a2cf6d1b51d5b5dcca0b8ee262126270'),
 'source/src/cryptalis/_experimental_public_update.py': (10285,
                                                         'bfd2e84e30acab549f7b221110b7bec3aa150bc16084669ea32a462a4e8c20c3'),
 'source/src/cryptalis/_native_text.py': (2237, '39460e5f75f72b15c8f98c5b4c333a18a432668990f31bc80f0c6887c1bbd170'),
 'source/src/cryptalis/_object_comments.py': (12999,
                                              '00c6bc68768fffc813bdfa4ee5302e93d4f76a9754b7b704955cf186c978192c'),
 'source/src/cryptalis/_sqlalchemy_guard.py': (4807,
                                               'e4dfb340fadb36ba2544267e714e2414c465bf64313ae6b27c058d1da4c7f819'),
 'source/src/cryptalis/_sqlalchemy_search.py': (9557,
                                                '857bb89d2f0aae0dc8b41f7c14bcc9dcd5285640fbe0969fbd8421ef2059ee63'),
 'source/src/cryptalis/_sqlalchemy_transactions.py': (8273,
                                                      'cb128481811576d8f16b233d4a30fca060eb9a1bfc4459d5e7e129434cc522ec'),
 'source/src/cryptalis/_sqlmodel_support.py': (2566,
                                               'c3b30313e0078bf39b16eef15802fb412d5f5ac9dc10938fa4c311fcb9ac449d'),
 'source/src/cryptalis/_transition_json.py': (2150, '2110f79fc1f38500daaaa2da814224afda9a9a92a5e8e776420d9168736d8a19'),
 'source/src/cryptalis/cli.py': (17882, '0df0b4f0101933b3a069024965b7bc5a3374747aff53d37099d2f22efc105efe'),
 'source/src/cryptalis/contracts/__init__.py': (58, '7a621ddfa3ed2dd543a3495b8cedaed3f892fc6b1fae0b6e8d04285741bd8660'),
 'source/src/cryptalis/contracts/active_state.py': (8925,
                                                    'b22608114fda5f49b2fa054fef24763bc9735c37612edfce0b13e16ca0df7532'),
 'source/src/cryptalis/contracts/development_authority.py': (3337,
                                                             '1fe8519fe06fd0121829b92e04f1b5be2b8b72e39f3b8eecc3d60b6e168810d7'),
 'source/src/cryptalis/contracts/transition.py': (6485,
                                                  '407c8028827ac7660cf6c4d3d4cfae30ca2dacf69ca80749e4e52f07d5c3d923'),
 'source/src/cryptalis/crypto/__init__.py': (961, '15ab27443d10863330631cf53c48e5643934919e470f9e2138db7f59434befc2'),
 'source/src/cryptalis/crypto/_candidate_envelope.py': (3964,
                                                        '9c28cb84a85123130328b2273eb27786a95f7953a41f0ec27f1c11100e28e55f'),
 'source/src/cryptalis/crypto/_candidate_scalar.py': (7050,
                                                      'b97a21a29b4bc9453af8c4c0a8f22b4860892b85854b5d1196ebca2f5094269a'),
 'source/src/cryptalis/crypto/_candidate_wrap.py': (3518,
                                                    '18cd89777178a5938848c51d47b48603dab902f57e83a6b330a8643f92748dc4'),
 'source/src/cryptalis/crypto/_payload_rotation.py': (5027,
                                                      'eb1117e9f03710bcd04d4139c181930102573c5f3de7f9167a7178c2660c295e'),
 'source/src/cryptalis/crypto/_rewrap.py': (2708, '797d1789c983e8c4eba36a792c8d4b5c00cba734bd25b61d6a970f1711be734b'),
 'source/src/cryptalis/crypto/cf1.py': (9977, 'd74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278'),
 'source/src/cryptalis/crypto/development_file.py': (5207,
                                                     '12e3ace1bf41a551c3ce98719c1b6f06aa004125afb79f72eed1e746f6b858a4'),
 'source/src/cryptalis/crypto/keys.py': (14233, 'b76d60f32011705726cc73f6211fa52e5624e475fc63573e578aa9e5078aea56'),
 'source/src/cryptalis/cutover.py': (12254, 'bef95a5d97b256ea1fa56565fcb9e1a1d2786748757777cf366b453d3cf42783'),
 'source/src/cryptalis/deprotection.py': (32239, 'f84a551eb27fe238ecaed3a21d468e243e31d20674b8965c5ac7ce421e04a16a'),
 'source/src/cryptalis/doctor.py': (11085, 'c2f4e7523ffe496bd8d0bac44d541c24bf532eea78e8cd42823014dae6875a72'),
 'source/src/cryptalis/manifest/__init__.py': (79, 'd2dc8653181d66161df9d9eb29ea79fb36b38fd93848d4da4a25184cda6885cd'),
 'source/src/cryptalis/manifest/canonical.py': (759,
                                                '6fe7e3d22cece14e5d85de912acdaf782a5421bfaa5c4dd796f78ab5bd4c2ec8'),
 'source/src/cryptalis/manifest/compatibility.py': (24725,
                                                    'ba8ce979234426f0e16961fa065fd54dda7bceb50c7019e2bc5e11b33d092920'),
 'source/src/cryptalis/manifest/compiler.py': (51172,
                                               'dca174cba23517abfcb03e8a1df7ef12f9f7e1171b765e3c1b2da26edb23951b'),
 'source/src/cryptalis/manifest/declaration.py': (7156,
                                                  'ea4162c8686f46ad8fe1ffdd1500186c55a3f4eee861469e64de603dca79d35b'),
 'source/src/cryptalis/manifest/descriptor.py': (2984,
                                                 '739d0438451c47746850c6aa488add4cfd7782ddeebd743741cccd290d2ce20d'),
 'source/src/cryptalis/manifest/header.py': (5449, '6e450d8565e3d7c19ecedd6c6b3120715ea5c7ee3b1ee439fef9e5080bb5eb6a'),
 'source/src/cryptalis/manifest/parser.py': (3380, '47cd75cc2ca611fe186d36d5d046317b0746714945c11fd2f84917d2f1020448'),
 'source/src/cryptalis/manifest/routines.py': (4219,
                                               'aad088b76dc9f2a16604d80d1210d80b99e9efb691948b0392bfcd881f73c4b8'),
 'source/src/cryptalis/migration.py': (51082, '5db6aed86a8bab6576582eaace940aae4ca022ec79b744c55bc6be2c5a4d6967'),
 'source/src/cryptalis/sqlalchemy.py': (65537, '6a9b7b5a6bf2f16fe254134f228531188ab02dae16201e87c15a6537d07dfa30'),
 'source/tests/async_sqlmodel_oracle_support.py': (10075,
                                                   '28a8eb13d10c5ea717cf2f88fd391c52f40cd834b2f2790bdb66f1da6404ab09'),
 'source/tests/conftest.py': (1584, 'fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd'),
 'source/tests/deprotection_native_worker.py': (1252,
                                                '4e8831ad2673a1a962dc1d4898ffe98aaa6d27becf990bbb81188015edea9d7d'),
 'source/tests/deprotection_worker.py': (1237, 'eb40b2c4c79834948cbf9799b05c901ff22ad516c146e3e18087ffb619756346'),
 'source/tests/fixtures/cf1_vectors.json': (28718, '24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e'),
 'source/tests/migration_commit_proxy.py': (4660, '9d904aa020dac32413689e2b16d2dce06e654f07f16c969cc565fbdb385a6fbb'),
 'source/tests/migration_worker.py': (766, '033b592d725ec574bd430538046eae46a887b485309ed17bddcbbacb79558735'),
 'source/tests/profile_membership.py': (8138, '94ce19cc8df73876a099751b6cffd4a6bfabf40f9bf44192a1c6956955a1ad75'),
 'source/tests/profile_migration.py': (7680, '27180a224858a65a8b671e65541d710c76c488eedd7d61bf3902b3274c06ed81'),
 'source/tests/profile_migration_step_a.py': (15671,
                                              '69a5d7326184875f36004366df5f1db0cf1c780c49c82559835dc40490087cf7'),
 'source/tests/profile_sqlalchemy_adapter.py': (13895,
                                                'e86690838c256d0e16b1ef498d154d3616f66960ca6a5215f01f61e734d2bed4'),
 'source/tests/profile_sqlalchemy_search.py': (20874,
                                               '19445c1ea169728af07630734d3c2dba8f5ece7679907899ff0105de16180692'),
 'source/tests/reference_cf1_vectors.py': (12714, '7be77c31e92ffb7255900b01e4b895ed40c935049ad2063c848492444c7e8e19'),
 'source/tests/regress_migration.py': (6793, 'b00267c6b1d507bc7cf66f983083c06b191d92e6c4f68dd618405f040d38e677'),
 'source/tests/regress_migration_corrective.py': (7994,
                                                  '3729a3f2186faf16e655b271a1f9a74eee8e92c031af40bc97f56693d1a9828d'),
 'source/tests/regress_migration_lock_queue.py': (5474,
                                                  'f13556f0bc5f0636bc8ca5c0f11b519c3e0dbb9376437ca450a7643e8d1df6c6'),
 'source/tests/regress_migration_membership.py': (4054,
                                                  'c2bae8a71fea8f9e65f753e8d879c509611e0dad03f5ce38ebcd663e4c4790ca'),
 'source/tests/regress_migration_pause.py': (5590, '8d4b3b0a642e383bc1754d0369fecd7ee926283492b90e16be64d6fa4bb86cc8'),
 'source/tests/single_tenant_public_cascade_fixture.py': (4477,
                                                          '346d4693e51a63a74e215cc3e823e094996066cbcb0f07a9eb2233fa091d48b7'),
 'source/tests/test_active_state.py': (10920, '6f57b46391a880b1c3dc2eeca8277baef3143eda7e99b56c05c95811c335b466'),
 'source/tests/test_adoption_diagnostic_currency.py': (2362,
                                                       'd2d744a6d48a71b4e094a9637b3d14f3dad134c23c38683783649248f8121011'),
 'source/tests/test_async_sqlmodel_public_hook.py': (35646,
                                                     '1e3a49fe28ecf0d41ecf739ec260ff4378f5ab03c463615c90fa91771eb715b7'),
 'source/tests/test_attachment_engine_preflight.py': (5031,
                                                      '118c49e0ef14b30ecd4d35e43c0458a33382c765e5610342b488b6d88756ef86'),
 'source/tests/test_candidate_envelope.py': (7572, '0719e40a1fd9ab123ea601d4c4177287101a8984efe282ee786200464628b860'),
 'source/tests/test_candidate_scalar.py': (14141, '7230944955a67c2ee91cf170b7ff2f280fc0c76bdfd56c97882d8110d5c277b5'),
 'source/tests/test_candidate_wrap.py': (6941, '85aa66f3e2ed625e20f13eedc1a41b38049c0ef4b9815928c878f9b943ba8457'),
 'source/tests/test_catalog_search_path.py': (9250, 'eae05b0f2bc1940ab382f47c499ad281de9972d44b67b7e3f2cc0554a8e184f0'),
 'source/tests/test_cf1.py': (23069, '911a67a9d98e8e61fb215e913b038d4dd820ba414cd14c1ec6f30e374044ecf2'),
 'source/tests/test_cf1_backend_failures.py': (4970,
                                               '960a3048895b4b4ce272630a5870f1443ab25a252e26dcb48dfb0a1366135a1e'),
 'source/tests/test_cli.py': (25921, 'd013dce84a813bdde34917a2778d1669bdd89e7960dd975f22905a2b5e8a0ca9'),
 'source/tests/test_cli_history.py': (10267, '44b0886c98b3031fa6e18499f456f162b69bd5424b4c7e88bc670d97af379df5'),
 'source/tests/test_compatibility_namedexpr.py': (3586,
                                                  '05b69558fd5b72781f81f63c48ba1c46f6307f4b2f0cc0e6d653d7735dbb2eef'),
 'source/tests/test_compatibility_report.py': (9577,
                                               '1d220fa656af7d2120440572b60d7a2388ecac7c075dd8a59372f2722f62910b'),
 'source/tests/test_compatibility_statement_bindings.py': (6267,
                                                           'f5a20b9a49ce5dc0c36199d41a0811ef8115bdd5c58685052fe33b89dd787cbd'),
 'source/tests/test_compatibility_string_bindings.py': (6374,
                                                        'fea21ff5374d165112d4370514fbdd430f708db96635e0aea2d4f9aff22f1ed8'),
 'source/tests/test_database_diagnostics.py': (2183,
                                               '69c1faee437d1940edfb2a216ea5f350b7447fabda2286e20118fa09139fd4ff'),
 'source/tests/test_deprotection.py': (26710, 'a7bcc6d2c1dad5161f76a49e19c565481f78ebce2608af768f98b5deb1e93d32'),
 'source/tests/test_deprotection_ordinals.py': (5528,
                                                '4855458d1b0847c353accab010b8521cc7374601f272340df8b2367ea8ea9cd5'),
 'source/tests/test_development_authority.py': (5178,
                                                '7ec9747dd8e5f4c9bffe073a777f70388c3b2d8c9ca22b9c2d9af95d0c49ea80'),
 'source/tests/test_doctor.py': (6832, '8a546981a1d154fd39245cf5cdee773a64c6d191a2905aa18a84a459aa711f20'),
 'source/tests/test_doctor_active.py': (6724, '82765e928801c5f0f2c65ea43db94a6245d06679dc72260ebf356dfac2f8715a'),
 'source/tests/test_doctor_ciphertext.py': (7877, '172fc0e8ae2a8f3dbce44d5eff7648094ad53a5c6c3de4ea217459a1a43f4acb'),
 'source/tests/test_doctor_setup.py': (16410, '1f6c10d1e470dac43a352f436e98bc57bd3af9fd8e662a8dfc45875815f9d833'),
 'source/tests/test_doctor_snapshot.py': (4179, 'bc2749571dc2941878e53e6bb02c4e4f5b0b841480ed3df39f43c471771e29d2'),
 'source/tests/test_file_development_provider.py': (6449,
                                                    '4d4e51ffb221a218fe6b1a91ce0d42ab65c5126d3ce8c746a1d4a36f43d57cc4'),
 'source/tests/test_file_provider_postgres.py': (3646,
                                                 '7fc0923d2efcc57b1c351fb838fb2737651ba4e054c47fe6c9e6fd1c50fcca4a'),
 'source/tests/test_key_lease_renewal.py': (4441, '68fdae216597da746dc659ed8a0de0dfb30469094a9090a02d60fda10196e113'),
 'source/tests/test_maintenance_budget_boundary.py': (6567,
                                                      'ea8e48b6304887d65df72d0b0d0ad3ee99a4fd97bfabfa13aedc32693129ab81'),
 'source/tests/test_manifest_canonical.py': (8454, 'f95532844a798f986c44034096625eccd835a13d0df9c0c3befc0a3d5d4cc1e9'),
 'source/tests/test_manifest_header.py': (6564, 'd3d3724688f7ed790e35f253bce9cab77909f42819355e16f7a59e5e8b55cb8f'),
 'source/tests/test_manifest_parser.py': (5201, '3028e621d207b5e1435f504bada3a465720993c41681b7422978750de75dd0f7'),
 'source/tests/test_migration.py': (43808, '523cad2b77b760f01a52d8a7c96cb3005e56254af44be60e00b684d14ed8105c'),
 'source/tests/test_migration_audit.py': (12244, '77a275b649b1745bf5ecf02d2938098c1a3bb424917cac489bc63ef3ce93edc5'),
 'source/tests/test_migration_byte_bounds.py': (7040,
                                                '8eaebefa3df2fa06c752e3d2594065edbce0b46cb6cc370f86b7613dd81c92b7'),
 'source/tests/test_migration_fault_selector.py': (869,
                                                   '7ee5265df9c66bd992d6ecec8fd878fa71a832ee7ec26db6286a4ce65f9883c8'),
 'source/tests/test_migration_key_leases.py': (5769,
                                               '574005b19b30d62e96fa2f536dbd645701ef996b1afca6339110a3aaafbef96d'),
 'source/tests/test_migration_lock_queue.py': (12013,
                                               'da4a1f20a3b077900761124853121a348e930569198437b289d60ce26b693197'),
 'source/tests/test_migration_membership.py': (5004,
                                               'a6ec0e602bbea264a1af29b6608a44e782aca7d7fac9a6835c58ea0766e6b623'),
 'source/tests/test_migration_multitable.py': (18962,
                                               'bda36abba7f1aed88430b34f49dfab98657b2baffad19e29dc671922159b3891'),
 'source/tests/test_migration_pause.py': (8057, '870e8c9bb4a274cb1ba946d83e714227de527683d001d8e47345fac009ef6e8e'),
 'source/tests/test_migration_plan_diagnostics.py': (1457,
                                                     '38e3b1aa5a3e2dc4b0978d3e01df0c29f53015c776dcbab6c6345766094ef0b6'),
 'source/tests/test_migration_role_template.py': (1200,
                                                  'c5229750cc28a970cafea1e4c769bddc0db07dfe5de46088618747598be0766f'),
 'source/tests/test_migration_runtime_privileges.py': (6916,
                                                       '3fba8a3efb78ad2b1287a063ffa2da648738d3f010e205b10486cf8baeedf436'),
 'source/tests/test_migration_snapshot_boundary.py': (4138,
                                                      'ec0d5fa61fdc5e14e81763ad07b5cdd8581411e31602250069b228249df2487a'),
 'source/tests/test_payload_rotation_preparation.py': (18913,
                                                       'eb841213900dd279efbfcbc47c18c99e5fa714308f594f65e3aa335c71be481a'),
 'source/tests/test_plan_estimate_bounds.py': (3147,
                                               'b9fb83970dc1fdeb65d07503bb6da278d5537b51e7da129516a6b792d809b47a'),
 'source/tests/test_plan_provider_snapshot.py': (8046,
                                                 '58f9f1e5b2226944ba9dc10d23d4b250a9b49a1c49a6f601f86a9d8b3bf54802'),
 'source/tests/test_private_public_update.py': (23559,
                                                '44b03cbee5469cab0ac3b5dc7d5e870f2adf12aba73e89b3947f6a445e3b25a6'),
 'source/tests/test_private_public_update_faults.py': (26148,
                                                       'b02b835db801c7b0bc735323ea91e058ed8d2bc1e3408b39604ea1aa280281e6'),
 'source/tests/test_protection_compiler.py': (24656,
                                              '5ff497e6e052c33204cfe251313407304459467b2d5e5286269b817a38222587'),
 'source/tests/test_protection_declaration.py': (5546,
                                                 '23e047858168d10d5788aaf5bcbd5af867e35cef2f8b4e035ed616b2015fdd38'),
 'source/tests/test_query_capability_survey.py': (7371,
                                                  'c87ef2c5b9fbc9e4dafb79ab77be5c275737e3a2c1764b7f1d1e431919a09f4a'),
 'source/tests/test_removal_input_diagnostics.py': (5549,
                                                    'f87f4afdb5d8b9971b71cbd0961a7f9c411f681a06bbb67c279354dd7fdd4fe3'),
 'source/tests/test_retained_profile_safety_oracles.py': (16240,
                                                          'e5467ca180f679abcedef5dc105690aa64912900cf43ee46c4935c715fddbfae'),
 'source/tests/test_retained_public_metadata.py': (6862,
                                                   'e55ed82ba4b9183c81bd24577fcf05f6ed123de86f3c9b46610dc914b4f424a9'),
 'source/tests/test_retained_schema_errors.py': (6527,
                                                 'ba7a4869e0017ca0b812bbe1025d0f325ba578e407f948b0a2803166a31fa215'),
 'source/tests/test_reverse_policy_drift_recovery.py': (8476,
                                                        '22c0d97956346dd606abdf1de88e1d605917741868b3f0fe45aeeaa6f188eeb5'),
 'source/tests/test_reverse_predecessor_consistency.py': (9711,
                                                          '1f90dae3613cd57bcb9817af6da2411e26134227b1c3681303b6dd46e8a1017d'),
 'source/tests/test_rewrap_preparation.py': (5058, 'd46556cc48301421c6bfeea7f7fa5624cf9f8bead9ae5e84ffaa5a2dd63b9a19'),
 'source/tests/test_routine_admission.py': (9056, '2fbc94ce31745497c5f52294e87d5b28cf2c9ea4859d9d55d1ab776d7e62ab01'),
 'source/tests/test_smolink_crypto_demo.py': (8843, '9410b81569287ab90534db2fac92edb932e7a38000e0a4caf0433ccb61a1ccb1'),
 'source/tests/test_sqlalchemy_adapter.py': (69975, '3f6deb6e0837596c0db6e8ebf19db19c042276bc091304e85766886184ef0c50'),
 'source/tests/test_sqlalchemy_async_cleanup.py': (7900,
                                                   '19191d11b6c02774bb3b3ce449c09b526a87ddf1c8730eb3393578c58cd5e789'),
 'source/tests/test_sqlalchemy_async_collection_methods.py': (5802,
                                                              '731278111ce02f66f18f15a5d6e17bd287607eaa019786718a4eb1099d6335be'),
 'source/tests/test_sqlalchemy_async_exit_double_failure.py': (17123,
                                                               'b01604d52da66697da025fe2d752b14700d304a3123408bb19b24c8863cf5978'),
 'source/tests/test_sqlalchemy_client_default_boundary.py': (16861,
                                                             'b12997edabab634c01c8b26f8f946392a70503d55389fa6cd826f979b33535e2'),
 'source/tests/test_sqlalchemy_core_autoflush_boundary.py': (4362,
                                                             'b27c4b2256db7595eafabb7477cdbd259b69a91e977bfa7b03a6848f3cb5cf4e'),
 'source/tests/test_sqlalchemy_flush_preparation_failure.py': (12508,
                                                               '8e86b882cc1a41d3a0971fa0b4f58e696ccf9e5c9647ed0844e21168c2055ee0'),
 'source/tests/test_sqlalchemy_negative_predicates.py': (6461,
                                                         '7578af71af7c774ad6c03d327d8bbe1f6fc5c605511b59062a4306667ff7fb20'),
 'source/tests/test_sqlalchemy_optimistic_versioning.py': (9865,
                                                           '763ee88b0d01ea8e64cdcae9b3c55b5052a39ac4fe14f24492f06544e2a55d96'),
 'source/tests/test_sqlalchemy_ordering_labels.py': (7167,
                                                     'dcd8eba3c0f1c3315e28834b1b6d0674b36479f31cf6cd94ea6293e6b1b0a83f'),
 'source/tests/test_sqlalchemy_outer_nulls.py': (8057,
                                                 '21a75523e968dde650f3082c08ca25d8355fbdd50cff7335ed33471fc3bc5abd'),
 'source/tests/test_sqlalchemy_provider_implicit_flush.py': (4229,
                                                             '052ecfeba2d7df358433be89545222d73e7c8816fa09b667fe4ceec4e282a3a9'),
 'source/tests/test_sqlalchemy_provider_no_flush.py': (2643,
                                                       '536f14671cb3c80e0f550464088cda73d6dc808985d292fc1c99a5073cf4a746'),
 'source/tests/test_sqlalchemy_savepoint_faults.py': (4966,
                                                      '93f6d6ec618205eed0e0964054bd26a6e1eba594771b378ddf65edd99c2514ff'),
 'source/tests/test_sqlalchemy_savepoints.py': (12458,
                                                'cf30f6d79d3e8b5b03bca7c0c777a9886754294cc5fe1ee617385d5922857977'),
 'source/tests/test_sqlalchemy_search.py': (65223, '0d9de8f210d482db210b982e0aa2b027e989e0deb589114a753ee4dfbf869015'),
 'source/tests/test_sqlalchemy_session_execution_options.py': (3944,
                                                               'fd07afde8c59159dcb888c2c67fc74a2030b9da4f77db915e51453fd1dc407e6'),
 'source/tests/test_sqlalchemy_thread_isolation.py': (3352,
                                                      'ab4137ee0a0b3e570b2a712d6c230bf14cdd03171bd5c5c2ddf4701fb900dfb3'),
 'source/tests/test_sqlalchemy_versioned_savepoints.py': (10095,
                                                          'fb5556204289e677b8b688af8ff28111ea8766477d99e8cd5482f54499efd143'),
 'source/tests/test_textual_clause_boundary.py': (7451,
                                                  '68cad71a86f5d7471c32a3bdafa0da72ec751530f6b451a50412aa20e109f4fc'),
 'source/tests/test_textual_from_boundary.py': (6121,
                                                '43bf89c1e5030101c8d590db4a4c56fb1eb4b2514ee184a2b868f3eb9ec009bf'),
 'source/tests/test_textual_group_shadow_boundary.py': (946,
                                                        '9ffbbc24c425d76b060ba22d3cf2d744df97bb2278728ea5adadc342e9611aa6'),
 'source/tests/test_transition.py': (6658, '54180b2df385b9fba43144bfab097d921e1b4510823ed7447be396c7aedf9f93'),
 'source/tests/test_transition_rate_estimates.py': (4518,
                                                    '263ef93fdc5d03d54eb825056ec939c9757cfede399045b73248c923c5e4dfad'),
 'source/tests/test_tuple_encoding_oracle.py': (1133,
                                                'c2081959dffa691828aba498beeb77398c6489c6ebc935b626de71758bb45b40'),
 'source/tests/test_unqualified_public_child.py': (7554,
                                                   '5dca9ee725d581bffbfc07c93251eca9d954bc10a6ae1b8b3aac9d46d56d414b'),
 'source/tests/test_unqualified_public_child_async.py': (3142,
                                                         '6fc0fa244d8f0beed24cad10b300bfbfbc69f582ecde58a314a97042db3132a5'),
 'source/tests/test_varchar_admission.py': (2003, 'f3ff42c473cd2c3a7202d9395a9feedfa9b595004b48298d19ecfb303e0cf3c7'),
 'source/tests/test_varchar_failure_boundary.py': (2653,
                                                   'b0230c062e19ba039746149fd212f965e397205ee599bdd145bed8f0775efe7f'),
 'source/tests/test_varchar_lifecycle.py': (2328, '4d79a9df05fa16fc4f6bceb663ec4314ba4ff8b7a3e5bf87e7471b3d2f45b35e'),
 'source/tests/test_varchar_runtime.py': (1874, '7357c5e27e8503b3f5aa4fc07af31e04ffa280e690bb336fbcb5eeb43c3fd53a'),
 'source/tests/test_warm_mapper_attachment.py': (1899,
                                                 '7c680799d576f90f1dd91a7f8d94a9957401297d9b1b7f96a58ae67f8de7ae5f'),
 'source/tests/test_warm_worker_maintenance_fence.py': (7532,
                                                        '7aa02c574306951bfec0932699d1fd27fdd31efe702754cf144b04ae0120a30f'),
 'source/uv.lock': (103898, 'faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e')}
BASE_PART_MANIFEST_SHA256 = '95283f84eebc99775c574a6c2bc6c832c20bd9cedbe0edffdc5f4109adb24ca8'
EXPECTED_BASE_REMOTE_FILES = [('MANIFEST.json',
  2964,
  '95283f84eebc99775c574a6c2bc6c832c20bd9cedbe0edffdc5f4109adb24ca8',
  '7c12ae61f986c0a8b81e135fe9ce60c7f13253ef'),
 ('part-01.bin',
  96000,
  'b51274be79d8eff24dc5721bd6a87d77aa52072f834c205a9115638f2822397a',
  '0dcab85978256326c767d5a3e457645f5f0a4f18'),
 ('part-02.bin',
  96000,
  '929aa55505f8838316e20b45cfd39ff60d4fd8cbfc4633d915d8348dd2d3dfe3',
  '785e2a7b50426c0f27bef562828faf9f3683ba97'),
 ('part-03.bin',
  96000,
  '168e6df70da63ec21ec1f196a81a8e526e87da4b76d86b624da39e21922e7d15',
  '44a0764e78421fded21781a2258370f65f5c2dfa'),
 ('part-04.bin',
  96000,
  'eb2f5efeea31f82742e99b970f44ff47c42a1d100e83d093778ba01ccdaf8a80',
  '0dfc10f58e27864e14f2c4aad8cc2909589ad237'),
 ('part-05.bin',
  96000,
  '017298da0170094ae3beb1d66bb110c04107f2b49eb769bab30ce48b40c22898',
  '3eb877ad43417c7d70a7fcc344cd4ad250d34dd9'),
 ('part-06.bin',
  96000,
  '8502cecb4d85a5e503000482609f095b61fab6d5e525ddf5ce7c1e0ecfa22a6e',
  'f05d199956353a71cb47d13dbcf6fded0b2d3240'),
 ('part-07.bin',
  96000,
  '91208c5da9e232fbfb66fbe77b5b667c50fcdd84983b09b5dcc038cd7ad1d07b',
  'c2b7807cd7e37d223bced1528eb76e801421f705'),
 ('part-08.bin',
  96000,
  'd5aeefbdb45a8c73b3313954c24926b4e85c79b6eefc6613067762f074747628',
  '9da15ff11979148c592cdb466a405506624ec32f'),
 ('part-09.bin',
  96000,
  '79fd6007c478c3d4d5961aae280442b82089bcf083a5325857406721b31c8174',
  '45c8a5bc2c0c10a9828ed21c74f5dfc4fbaf100a'),
 ('part-10.bin',
  96000,
  '826a9b32b442d066e731d3ae075d4c03f915326476a5a5025e878b82d4e08e29',
  'd783c64af462a46262e94677d5328b2de24bbd1d'),
 ('part-11.bin',
  69680,
  'b31cfc7364dc33639437364f52903cd3232f0697af06bd0522b750a02b91b37c',
  'e9133e032d78b18107de18de23cd6b353fc3ed65')]
EXPECTED_BASE_RESTORE_REPORT = {'all_restored_files_mode': '0600',
 'all_seven_gates': 'UNKNOWN',
 'archive_bytes': 1029680,
 'archive_code_executed': False,
 'archive_sha256': '1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af',
 'authenticated_provenance_sha256': '93b32a8e71db994724409f506c3040e3aad64c9b03a650cf14df7f970e1d7995',
 'authentication_scope': 'Exact externally authenticated and independently pinned commit plus twelve per-file readback '
                         'receipts; this offline checker cannot authenticate a network service or distinguish '
                         'dishonestly relabeled staging bytes.',
 'complete_name_type_header_bounds_before_member_body_reads': True,
 'complete_output_and_input_readbacks_verified': True,
 'exact_allowlist_sha256': '8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176',
 'exact_regular_members': 516,
 'extraction_directory': '/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/async-cleanup-focused-remote-fresh-extraction',
 'focused_recorded_results': {'green_sa20': {'nodes': 46, 'passed': 46},
                              'green_sa21': {'nodes': 46, 'passed': 46},
                              'red_sa20': {'failed': 13, 'nodes': 22, 'passed': 9},
                              'red_sa21': {'failed': 13, 'nodes': 22, 'passed': 9}},
 'frozen_manifest_sha256': 'e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174',
 'full217source_directory': '/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/async-cleanup-focused-remote-full217source',
 'full_matrix_qualification': 'PENDING_SEPARATE',
 'full_suite_current_run_included': False,
 'green_source_hashes_verified': True,
 'historical_seven_acceptance_failures': 'Unresolved prior disposition preserved; not rerun or reclassified.',
 'independent_archive_review_sha256': 'cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a',
 'installed_qualification': 'PENDING_SEPARATE',
 'member_bytes': 9148868,
 'new_secret_scan_performed': False,
 'operational_environment_restore_claimed': False,
 'part_manifest_sha256': '95283f84eebc99775c574a6c2bc6c832c20bd9cedbe0edffdc5f4109adb24ca8',
 'parts_verified': 11,
 'product_imports_tests_network_git_databases_subprocesses': False,
 'recorded_results_scope': 'Preserved accepted byte evidence only; no fresh runtime result or separate node '
                           'reconciliation is claimed.',
 'red_and_baseline_byte_reconstruction_verified': True,
 'remote_commit_sha': '86fb0e26ac4032a405b8c077939eb3e288e69db5',
 'remote_files_verified': 12,
 'remote_prefix': 'recovery/async-cleanup-focused/parts',
 'repository': 'debgh-workspace/cryptalis-research-lab',
 'restored_full217source_bytes': 4423405,
 'restored_full217source_files': 217,
 'runtime_dependency_database_state_restored': False,
 'security_qualification_or_universal_quarantine_claimed': False,
 'status': 'PASS_COORDINATOR_AUTHENTICATED_REMOTE_DATA_ONLY_CLEANUP_RESTORE',
 'synthetic_fixture_disposition_sha256': '640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022',
 'synthetic_fixture_dispositions_preserved': 2,
 'tar_bytes': 9543680}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def hex_digest(value, length=64):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(length) + '}', value) is not None


def unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'Duplicate JSON key')
        obj[key] = value
    return obj


def reject_constant(value):
    raise ValueError('Nonfinite JSON number')


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def json_bytes(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + '\n').encode('utf-8')


def safe_name(name):
    require(isinstance(name, str) and name and name.isascii(), 'Empty/non-ASCII path')
    require('\\' not in name and ':' not in name and all(32 <= ord(x) < 127 for x in name), 'Unsafe path character')
    require(all(x not in ('', '.', '..') for x in name.split('/')), 'Unsafe path component')
    p = PurePosixPath(name)
    require(not p.is_absolute() and p.as_posix() == name, 'Noncanonical relative path')
    require(p.name.casefold() not in FORBIDDEN_LEAVES, 'Raw phase path forbidden')
    require(not any(x.casefold() in (FORBIDDEN_PARTS - {'toolchain'}) or x.casefold() == '.env' or x.casefold().startswith('.env.') for x in p.parts), 'Environment/credential/cache path forbidden')
    require('toolchain' not in {x.casefold() for x in p.parts} or name in {'workspace/cryptalis-executable/toolchain/lab_progress.py', 'workspace/cryptalis-executable/toolchain/run_baseline.py', 'logical-workspace/workspace/cryptalis-executable/toolchain/lab_progress.py', 'logical-workspace/workspace/cryptalis-executable/toolchain/run_baseline.py'}, 'Unadmitted toolchain path')
    require(not p.name.casefold().endswith(('.pyc', '.pyo', '.sqlite', '.sqlite3', '.db', '.pem', '.key')), 'Runtime/credential file forbidden')
    return p


def nameset(names, empty=()):
    require(names == sorted(set(names)), 'Names are not sorted unique')
    files, directories = set(names), set(empty)
    for name in names + list(empty):
        directories.update(p.as_posix() for p in safe_name(name).parents if p.as_posix() != '.')
    require(not files & directories, 'File/directory collision')
    require(len(files | directories) == len({n.casefold() for n in files | directories}), 'Casefold path collision')
    return directories


def validate_restored_entry_name(name, info, expected_directories):
    """Admit the one required toolchain parent only as an observed directory."""
    if stat.S_ISDIR(info.st_mode):
        require(name in expected_directories, 'Directory outside computed output closure')
        if name == 'logical-workspace/workspace/cryptalis-executable/toolchain':
            return
    # A file at that parent name, an unlisted sibling, and every other entry
    # still use the unchanged exact leaf exceptions and generic safety checks.
    safe_name(name)


def open_directory(path):
    require(path.is_absolute(), 'Directory is not absolute')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in path.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def signature(s):
    return (s.st_dev, s.st_ino, s.st_size, s.st_mode, s.st_nlink, s.st_mtime_ns, s.st_ctime_ns)


def read_regular(path, cap):
    require(path.is_relative_to(P), 'Read outside fixed recovery namespace')
    require(type(cap) is int and 0 <= cap <= MAX_STREAM, 'Bad read cap')
    parent = open_directory(path.parent)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and 0 <= before.st_size <= cap, 'Input is not bounded single-link regular file')
            data = stream.read(cap + 1)
            after = os.fstat(stream.fileno())
        current = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        require(signature(before) == signature(after) == signature(current), 'Input identity changed during read')
    finally:
        os.close(parent)
    require(len(data) == before.st_size and len(data) <= cap, 'Input size changed')
    return data


def absent(path):
    parent = open_directory(path.parent)
    try:
        try:
            os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            return True
        return False
    finally:
        os.close(parent)


def directory_entries(path):
    fd = open_directory(path)
    try:
        return set(os.listdir(fd))
    finally:
        os.close(fd)


def new_directory(path):
    require(path.is_relative_to(OUT) or path == OUT, 'Directory outside fresh output root')
    parent = open_directory(path.parent)
    try:
        os.mkdir(path.name, mode=0o700, dir_fd=parent)
        child = os.open(path.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        try:
            os.fchmod(child, 0o700)
        finally:
            os.close(child)
    finally:
        os.close(parent)


def write_new(name, data):
    parts = safe_name(name).parts
    parent = open_directory(OUT)
    try:
        for part in parts[:-1]:
            try:
                os.mkdir(part, mode=0o700, dir_fd=parent)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            require(stat.S_IMODE(os.fstat(child).st_mode) == 0o700, 'Output parent mode differs')
            os.close(parent)
            parent = child
        fd = os.open(parts[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), 0o600)
            require(stream.write(data) == len(data), 'Short write')
    finally:
        os.close(parent)
    require(read_regular(OUT / name, len(data)) == data, 'Output readback differs')


def create_empty(name):
    parent = open_directory(OUT)
    try:
        for part in safe_name(name).parts:
            try:
                os.mkdir(part, mode=0o700, dir_fd=parent)
            except FileExistsError:
                pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            require(stat.S_IMODE(os.fstat(child).st_mode) == 0o700, 'Output directory mode differs')
            os.close(parent)
            parent = child
    finally:
        os.close(parent)


def verify_tree(expected, empty):
    want_dirs = nameset(sorted(expected), empty)
    files, dirs = set(), set()
    root_fd = open_directory(OUT)
    try:
        require(stat.S_IMODE(os.fstat(root_fd).st_mode) == 0o700, 'Output root mode differs')
    finally:
        os.close(root_fd)
    for current, subdirs, leaves in os.walk(OUT, followlinks=False):
        for leaf in subdirs + leaves:
            path = Path(current) / leaf
            name = path.relative_to(OUT).as_posix()
            info = path.lstat()
            validate_restored_entry_name(name, info, want_dirs)
            if stat.S_ISDIR(info.st_mode):
                require(stat.S_IMODE(info.st_mode) == 0o700, 'Output directory mode differs')
                dirs.add(name)
            else:
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and stat.S_IMODE(info.st_mode) == 0o600, 'Output link/special/non-inert mode')
                require(name in expected and read_regular(path, len(expected[name])) == expected[name], 'Output member bytes differ')
                files.add(name)
    require(files == set(expected) and dirs == want_dirs, 'Output exact file/directory closure differs')
    for name in empty:
        require(not directory_entries(OUT / name), 'Explicit empty directory not empty')


def evidence_reference(value):
    return isinstance(value, str) and 0 < len(value) <= 4096 and value == value.strip() and all(ord(x) >= 32 and ord(x) != 127 for x in value)


def validate_provenance(raw, expected_hash, commit, prefix, path, archive_hash, split_hash, review_hash, rows, format_name):
    require(digest(raw) == expected_hash, 'Provenance differs from independent external pin')
    obj = parse_json(raw)
    keys = {'format', 'authenticated_remote_readbacks_verified', 'repository', 'remote_prefix', 'commit_sha', 'authenticated_commit_lookup', 'commit_lookup_sha', 'commit_lookup_reference', 'archive_sha256', 'part_manifest_sha256', 'independent_archive_review_sha256', 'local_readback_directory', 'source', 'local_staging_used_for_restore', 'remote_files'}
    require(isinstance(obj, dict) and set(obj) == keys and obj['format'] == format_name, 'Provenance schema/format differs')
    require(obj['authenticated_remote_readbacks_verified'] is True and obj['authenticated_commit_lookup'] is True, 'Missing authenticated observation attestations')
    require(obj['repository'] == REPOSITORY and obj['remote_prefix'] == prefix, 'Provenance remote target differs')
    require(obj['commit_sha'] == obj['commit_lookup_sha'] == commit, 'Provenance differs from external immutable commit')
    require(evidence_reference(obj['commit_lookup_reference']), 'Commit lookup reference absent')
    require(obj['archive_sha256'] == archive_hash and obj['part_manifest_sha256'] == split_hash and obj['independent_archive_review_sha256'] == review_hash, 'Provenance content/review pins differ')
    require(obj['local_readback_directory'] == str(path), 'Readback directory differs')
    require(obj['source'] == 'authenticated_remote_readback' and obj['local_staging_used_for_restore'] is False, 'Staging cannot substitute for remote bytes')
    require(isinstance(obj['remote_files'], list) and len(obj['remote_files']) == len(rows), 'Individual remote file receipt count differs')
    for record, (name, size, sha, blob) in zip(obj['remote_files'], rows):
        keys = {'name', 'repository', 'commit_sha', 'remote_path', 'authenticated_readback', 'bytes', 'sha256', 'git_blob_sha', 'verification_reference'}
        require(isinstance(record, dict) and set(record) == keys, 'Per-file receipt schema differs')
        require(record['name'] == name and record['repository'] == REPOSITORY and record['commit_sha'] == commit, 'Per-file name/repository/commit differs')
        require(record['remote_path'] == prefix + '/' + name and record['authenticated_readback'] is True, 'Per-file path/authentication differs')
        require(type(record['bytes']) is int and record['bytes'] == size and record['sha256'] == sha and record['git_blob_sha'] == blob, 'Per-file exact identity differs')
        require(evidence_reference(record['verification_reference']), 'Per-file observation reference absent')
    return obj


def authenticate_inputs(args):
    wanted = {row[0] for row in EXPECTED_REMOTE_FILES} | {'REMOTE_PROVENANCE.json'}
    require(directory_entries(PARTS) == wanted, 'Additive remote readback directory exact closure differs')
    snapshots = {}
    def take(path, cap):
        raw = read_regular(path, cap)
        snapshots[path] = raw
        return raw
    a_receipt = take(PARTS / 'REMOTE_PROVENANCE.json', 100000)
    validate_provenance(a_receipt, args.authenticated_provenance_sha256, args.expected_remote_commit, REMOTE_PREFIX, PARTS, A_SHA, PART_MANIFEST_SHA256, REVIEW_SHA, EXPECTED_REMOTE_FILES, 'async-cleanup-additive-authenticated-remote-provenance-v1')
    inputs = {}
    for name, size, sha, blob in EXPECTED_REMOTE_FILES:
        raw = take(PARTS / name, size)
        require(len(raw) == size and digest(raw) == sha and git_blob(raw) == blob, 'Actual additive remote body identity differs: ' + name)
        inputs[name] = raw
    require(parse_json(inputs['MANIFEST.json']) == EXPECTED_PART_MANIFEST, 'Exact additive split manifest differs')
    additive = b''.join(inputs[row[0]] for row in EXPECTED_PARTS)
    b_receipt = take(BASE_PROVENANCE, 100000)
    validate_provenance(b_receipt, args.base_provenance_sha256, args.expected_base_commit, BASE_PREFIX, BASE_PROVENANCE.parent, B_SHA, BASE_PART_MANIFEST_SHA256, BASE_REVIEW_SHA, EXPECTED_BASE_REMOTE_FILES, 'async-cleanup-authenticated-remote-provenance-v1')
    b_report_bytes = take(BASE_REPORT, 100000)
    require(digest(b_report_bytes) == args.base_restore_verification_sha256, 'Base restore report differs from independent external pin')
    b_report = parse_json(b_report_bytes)
    require(b_report == EXPECTED_BASE_RESTORE_REPORT, 'Exact accepted base remote restore receipt differs')
    require(b_report['remote_commit_sha'] == args.expected_base_commit and b_report['authenticated_provenance_sha256'] == args.base_provenance_sha256, 'Base report authentication binding differs')
    base = take(BASE_ARCHIVE, 1029680)
    require(len(base) == 1029680 and digest(base) == B_SHA, 'Authenticated base archive checkpoint differs')
    return additive, base, snapshots, wanted


def ustar_header(name, size):
    safe_name(name)
    encoded = name.encode('ascii')
    prefix, leaf = b'', encoded
    if len(encoded) > 100:
        for index, byte in enumerate(encoded):
            if byte == 47 and index <= 155 and len(encoded) - index - 1 <= 100:
                prefix, leaf = encoded[:index], encoded[index + 1:]
                break
        require(prefix and len(prefix) <= 155 and len(leaf) <= 100, 'USTAR path overflow')
    def octal(value, width):
        data = ('%0*o' % (width - 1, value)).encode('ascii') + b'\0'
        require(len(data) == width, 'USTAR number overflow')
        return data
    fields = [leaf.ljust(100, b'\0'), octal(0o644, 8), octal(0, 8), octal(0, 8), octal(size, 12), octal(0, 12), b' ' * 8, b'0', bytes(100), b'ustar\0', b'00', bytes(32), bytes(32), bytes(8), bytes(8), prefix.ljust(155, b'\0'), bytes(12)]
    header = bytearray(b''.join(fields))
    require(len(header) == 512, 'USTAR header construction differs')
    header[148:156] = ('%06o' % sum(header)).encode('ascii') + b'\0 '
    return bytes(header)


def admit_headers(packed, inventory, root, packed_size, packed_sha, tar_size, tar_sha, member_count, member_bytes):
    require(len(packed) == packed_size <= MAX_STREAM and digest(packed) == packed_sha, 'Archive identity differs')
    names = sorted(inventory)
    nameset(names)
    require(len(names) == member_count and sum(p[0] for p in inventory.values()) == member_bytes <= MAX_STREAM, 'Exact member inventory totals differ')
    for size, sha in inventory.values():
        require(type(size) is int and 0 <= size <= MAX_MEMBER and hex_digest(sha), 'Embedded member bound/hash differs')
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=DECODER_MEMORY)
    raw = decoder.decompress(packed, max_length=tar_size + 1)
    require(len(raw) == tar_size <= MAX_STREAM and decoder.eof and not decoder.unused_data and decoder.check == lzma.CHECK_CRC64, 'Bounded single CRC64 XZ stream/length/trailer differs')
    # Do not hash or index decompressed member bodies until BOTH complete
    # archive header passes have succeeded in main().
    positions, offset = {}, 0
    for name in names:
        size, sha = inventory[name]
        require(raw[offset:offset + 512] == ustar_header(root + name, size), 'Header name/type/attributes/size/order differs: ' + name)
        start, end = offset + 512, offset + 512 + size
        stop = end + (-size % 512)
        require(stop <= len(raw) and raw[end:stop] == bytes(stop - end), 'Member bound/padding differs')
        positions[name] = (start, end)
        offset = stop
    require(len(raw) == ((offset + 1024 + 10239) // 10240) * 10240 and len(raw) - offset >= 1024 and raw[offset:] == bytes(len(raw) - offset), 'Exact tar closure/terminal padding differs')
    return raw, positions


def read_member_bodies(raw, positions, inventory):
    payload = {}
    for name in sorted(inventory):
        start, end = positions[name]
        data = raw[start:end]
        require(len(data) == inventory[name][0] and digest(data) == inventory[name][1], 'Admitted member body hash differs: ' + name)
        payload[name] = data
    return payload


def verify_pair(ap, bp):
    require(digest(ap[A_MANIFEST]) == A_MANIFEST_SHA and digest(bp[B_MANIFEST]) == B_MANIFEST_SHA, 'Archived manifest identity differs')
    am, bm = parse_json(ap[A_MANIFEST]), parse_json(bp[B_MANIFEST])
    declared = {row['member']: row for row in am['members']}
    require(len(am['members']) == len(declared) == 355 and set(declared) == set(EXPECTED_A_MEMBERS), 'Additive manifest exact closure differs')
    for name, (size, sha) in EXPECTED_A_MEMBERS.items():
        row = declared[name]
        require(type(row['bytes']) is int and row['bytes'] == size and row['mode'] == 0o644, 'Additive manifest size/mode differs')
        if name == A_MANIFEST:
            require(row['kind'] == 'self-manifest' and 'sha256' not in row, 'Self-manifest contract differs')
        else:
            require(row['sha256'] == sha, 'Additive manifest member digest differs')
    require(am['member_count'] == 355 and am['payload_bytes_including_manifest'] == 38348976 and am['canonical_ustar_stream_bytes'] == 38635520, 'Additive manifest totals differ')
    require(bm['files'] == {n: {'size': s, 'sha256': h} for n, (s, h) in EXPECTED_B_MEMBERS.items() if n != B_MANIFEST}, 'Base manifest complete map differs')
    require(digest(bp[B_ALLOW_NAME]) == B_ALLOW_SHA and parse_json(bp[B_ALLOW_NAME])['exact_archive_member_names'] == sorted(EXPECTED_B_MEMBERS), 'Base safe allowlist differs')
    accepted_raw = ap['controls/independent/accepted-input-hashes.v1.json']
    require(digest(accepted_raw) == ACCEPTED_RECORDS_SHA, 'Accepted2386 logical record identity differs')
    records = parse_json(accepted_raw)['files']
    require(len(records) == 2386 and len({r['source'] for r in records}) == 2386, 'Accepted logical origin closure differs')
    flattened = {}
    for record in records:
        name = record['destination']
        safe_name(name)
        require(name not in flattened and name.startswith('workspace/'), 'Duplicate/unexpected logical destination')
        require(record['source'].startswith('/workspace/scratch/cb28ee9f5f4a/') and name == 'workspace/' + record['source'].removeprefix('/workspace/scratch/cb28ee9f5f4a/'), 'Inert origin/destination text mapping differs')
        require(type(record['bytes']) is int and 0 <= record['bytes'] <= MAX_MEMBER and hex_digest(record['sha256']), 'Logical size/hash invalid')
        flattened[name] = {'destination': name, 'bytes': record['bytes'], 'sha256': record['sha256'], **record['recovery']}
    nameset(sorted(flattened), [EMPTY_DIR])
    rows = parse_json(ap['controls/preparation/PROPOSED_RESTORE_MAP.json'])['files']
    restore_map = {row['destination']: row for row in rows}
    require(len(rows) == len(restore_map) == 2386 and restore_map == flattened, 'Complete2386 destination-keyed restore-map equality differs')
    require(sum(row['bytes'] for row in rows) == 65285835 <= MAX_LOGICAL, 'Logical byte sum differs')
    objects, references, logical, counts = {}, collections.Counter(), {}, collections.Counter()
    for name, row in sorted(restore_map.items()):
        member, kind = row['member'], row['kind']
        safe_name(member)
        counts[kind] += 1
        if kind == 'additive-object':
            require(set(row) == {'destination', 'bytes', 'sha256', 'kind', 'member'}, 'Additive restore-map row schema differs')
            require(member == 'objects/sha256/' + row['sha256'] and member in ap, 'Additive content address differs')
            body = ap[member]
            objects[member] = (row['bytes'], row['sha256'])
        else:
            require(kind == 'base-capsule-member' and set(row) == {'destination', 'bytes', 'sha256', 'kind', 'member', 'base_manifest_sha256'}, 'Base restore-map row schema differs')
            require(member in bp and not member.startswith('freeze/') and member != B_MANIFEST and row['base_manifest_sha256'] == B_MANIFEST_SHA, 'Base reference outside accepted eligible set')
            body = bp[member]
            references[member] += 1
        require(len(body) == row['bytes'] and digest(body) == row['sha256'], 'Logical resolved body differs')
        logical[name] = body
    require(counts == {'additive-object': 432, 'base-capsule-member': 1954} and len(references) == 253 and len(objects) == 295, 'Logical432/1954 and295/253 partition differs')
    require(set(objects) == {n for n in ap if n.startswith('objects/')} and sum(v[0] for v in objects.values()) == 27031716, 'Additive object closure differs')
    object_rows = parse_json(ap['controls/preparation/NEW_CONTENT_OBJECTS.json'])['objects']
    require(len(object_rows) == 295 and len({r['member'] for r in object_rows}) == 295, 'Object inventory duplicates/count differ')
    for row in object_rows:
        member = row['member']
        users = [r for r in records if r['recovery']['kind'] == 'additive-object' and r['recovery']['member'] == member]
        require(member in objects and (row['bytes'], row['sha256']) == objects[member], 'Object inventory identity differs')
        require(sorted(row['origins']) == sorted(r['source'] for r in users) and len(row['origins']) == len(set(row['origins'])) and row['source'] in row['origins'], 'Object canonical origin/alias set differs')
        require(declared[member]['canonical_origin'] == row['source'] and declared[member]['kind'] == 'content-object', 'Object manifest origin/kind differs')
    reference_rows = parse_json(ap['controls/preparation/BASE_CONTENT_REFERENCES.json'])['references']
    reference_map = {row['member']: row for row in reference_rows}
    require(len(reference_rows) == len(reference_map) == 253 and set(reference_map) == set(references), 'Base reference inventory differs')
    for member, count in references.items():
        size, sha = EXPECTED_B_MEMBERS[member]
        require(reference_map[member] == {'bytes': size, 'member': member, 'origin_count': count, 'sha256': sha}, 'Base reference multiplicity differs')
    eligible = {(size, sha) for n, (size, sha) in EXPECTED_B_MEMBERS.items() if not n.startswith('freeze/') and n != B_MANIFEST}
    require(not any(value in eligible for value in objects.values()), 'Unnecessary additive duplicate of eligible base content')
    controls = [n for n in ap if n.startswith('controls/')]
    require(len(controls) == 59 and sum(n.startswith('controls/preparation/') for n in controls) == 29 and sum(n.startswith('controls/independent/') for n in controls) == 21 and sum(n.startswith('controls/freeze/') for n in controls) == 9, 'Exact59 controls partition differs')
    require(am['logical_recovery'] == {'base_logical_uses': 1954, 'base_referenced_bodies': 253, 'bytes': 65285835, 'empty_directory': EMPTY_DIR, 'files': 2386, 'new_logical_uses': 432, 'new_object_bytes': 27031716, 'new_objects': 295, 'read_live_sources_during_restore': False, 'restore_map_member': 'controls/preparation/PROPOSED_RESTORE_MAP.json'}, 'Logical manifest contract differs')
    listing = ''.join('%s %d %s\n' % (digest(body), len(body), name) for name, body in sorted(logical.items())).encode('ascii')
    require(digest(listing) == LOGICAL_LIST_SHA, 'Canonical logical listing differs from final independent readback')
    packet = 'experiments/next-unblocked-correctness-20261014/'
    green = {n[len('source/'):]: body for n, body in bp.items() if n.startswith('source/')}
    source_allow = bp['freeze/preparation/SOURCE_FILENAME_ALLOWLIST.txt'].decode('ascii').splitlines()
    nameset(sorted(green))
    green_map = parse_json(bp[packet + 'GREEN_SOURCE_MANIFEST.json'])['source_sha256']
    red_map = parse_json(bp[packet + 'RED_SOURCE_MANIFEST.json'])['source_sha256']
    baseline_map = parse_json(bp[packet + 'BASELINE_SOURCE_MANIFEST.json'])['source_sha256']
    require(source_allow == sorted(set(source_allow)) and set(source_allow) == set(green) == set(green_map) and len(green) == 217 and sum(map(len, green.values())) == 4423405, 'Full GREEN217 exact closure/bytes differs')
    require({n: digest(body) for n, body in green.items()} == green_map, 'GREEN217 source identities differ')
    red = dict(green)
    red['src/cryptalis/sqlalchemy.py'] = bp[packet + 'BASELINE_sqlalchemy.py']
    require(len(red) == 217 and sum(map(len, red.values())) == 4421493 and {n: digest(body) for n, body in red.items()} == red_map, 'RED217 byte reconstruction differs')
    baseline = dict(red)
    del baseline['tests/test_sqlalchemy_async_exit_double_failure.py']
    require(len(baseline) == 216 and sum(map(len, baseline.values())) == 4404370 and {n: digest(body) for n, body in baseline.items()} == baseline_map, 'Baseline216 byte reconstruction differs')
    require([n for n in sorted(green_map) if green_map[n] != red_map[n]] == ['src/cryptalis/sqlalchemy.py'], 'Sole RED/GREEN source delta differs')
    source_categories = {'frozen-full-source', 'wrapper-source-archive', 'packaging-build-source-copy', 'packaging-clean-source'}
    copies = [r for r in records if r['category'] in source_categories]
    priors = [r for r in records if r['category'] == 'prior-corpus-archive']
    require(len(copies) == 1770 and all(r['recovery']['kind'] == 'base-capsule-member' and r['recovery']['member'].startswith('source/') for r in copies), 'Repeated source-copy mapping differs')
    require(len(priors) == 78 and all(r['recovery']['kind'] == 'base-capsule-member' for r in priors), 'Durable prior-corpus mapping differs')
    require(sum(r['category'] == 'accepted-review-and-method-history' for r in records) == 97, 'Accepted97 review/method history count differs')
    return logical, green, red, baseline


def main():
    parser = argparse.ArgumentParser(description='Offline fresh paired byte recovery, requiring actual remote provenance and independent external pins')
    for name in ['expected-remote-commit', 'authenticated-provenance-sha256', 'expected-base-commit', 'base-provenance-sha256', 'base-restore-verification-sha256']:
        parser.add_argument('--' + name, required=True)
    args = parser.parse_args()
    require(hex_digest(args.expected_remote_commit, 40) and hex_digest(args.expected_base_commit, 40), 'Expected commits must be immutable40 lowercase hex')
    require(all(hex_digest(v) for v in [args.authenticated_provenance_sha256, args.base_provenance_sha256, args.base_restore_verification_sha256]), 'Provenance/report pins must be64 lowercase hex')
    require(args.expected_base_commit == BASE_COMMIT and args.base_provenance_sha256 == BASE_PROVENANCE_SHA and args.base_restore_verification_sha256 == BASE_REPORT_SHA, 'Base external pins differ from reviewed checkpoint')
    require(absent(OUT), 'Fresh output exists; preserve prior attempts and do not overwrite')
    additive, base, snapshots, wanted = authenticate_inputs(args)
    araw, apos = admit_headers(additive, EXPECTED_A_MEMBERS, '', 2176040, A_SHA, 38635520, '115f914d680bb9f741145d9d4d45981b61d21b05f4876192435ef0c131160cb9', 355, 38348976)
    braw, bpos = admit_headers(base, EXPECTED_B_MEMBERS, B_ROOT, 1029680, B_SHA, 9543680, 'e7b50aa37b10c9162daabb78f80d4c5da07687ef4eb484154d79674f5edcf045', 516, 9148868)
    # BOTH complete header/name/type/size/order/padding passes now precede any
    # member-body slice, hash or parse. No archive-provided path grants reads.
    require(digest(araw) == '115f914d680bb9f741145d9d4d45981b61d21b05f4876192435ef0c131160cb9' and digest(braw) == 'e7b50aa37b10c9162daabb78f80d4c5da07687ef4eb484154d79674f5edcf045', 'Canonical paired USTAR hashes differ')
    ap = read_member_bodies(araw, apos, EXPECTED_A_MEMBERS)
    bp = read_member_bodies(braw, bpos, EXPECTED_B_MEMBERS)
    logical, green, red, baseline = verify_pair(ap, bp)
    expected = {A_ARCHIVE: additive, B_ARCHIVE: base}
    groups = {'additive-members': ap, 'base-members': bp, 'logical-workspace': logical, 'green217-source': green, 'red217-source': red, 'baseline216-source': baseline}
    for prefix, bodies in groups.items():
        for name, body in bodies.items():
            expected[prefix + '/' + name] = body
    empty = ['logical-workspace/' + EMPTY_DIR]
    nameset(sorted(expected), empty)
    require(len(expected) == 3909 and sum(map(len, expected.values())) == 129238667, 'Full fresh output data totals differ')
    require(absent(OUT), 'Output appeared before write')
    new_directory(OUT)
    for name, body in sorted(expected.items()):
        write_new(name, body)
    create_empty(empty[0])
    verify_tree(expected, empty)
    for path, raw in snapshots.items():
        require(read_regular(path, len(raw)) == raw, 'Authenticated input changed during restore')
    require(directory_entries(PARTS) == wanted, 'Additive readback directory changed')
    report = {
        'status': 'PASS_COORDINATOR_AUTHENTICATED_REMOTE_PAIRED_DATA_ONLY_CLEANUP_RESTORE',
        'repository': REPOSITORY, 'additive_remote_commit': args.expected_remote_commit, 'additive_remote_prefix': REMOTE_PREFIX,
        'base_remote_commit': args.expected_base_commit, 'base_remote_prefix': BASE_PREFIX,
        'additive_provenance_sha256': args.authenticated_provenance_sha256, 'base_provenance_sha256': args.base_provenance_sha256, 'base_restore_receipt_sha256': args.base_restore_verification_sha256,
        'authentication_boundary': 'Offline validation depends on independently pinned actual authenticated observations. The checker cannot authenticate a service or detect dishonest relabeling of identical staging bytes.',
        'additive_archive_sha256': A_SHA, 'base_archive_sha256': B_SHA, 'additive_manifest_sha256': A_MANIFEST_SHA, 'base_manifest_sha256': B_MANIFEST_SHA,
        'additive_part_manifest_sha256': PART_MANIFEST_SHA256, 'additive_parts': 23, 'actual_additive_remote_file_bodies': 24,
        'base_archive_input': str(BASE_ARCHIVE), 'base_parts_reread_or_relabelled': False,
        'independent_paired_review_sha256': REVIEW_SHA, 'independent_paired_review_closure_sha256': REVIEW_CLOSURE_SHA,
        'additive_regular_members': 355, 'base_regular_members': 516, 'both_full_headers_before_member_bodies': True,
        'logical_files': 2386, 'logical_bytes': 65285835, 'logical_new_object_uses': 432, 'logical_base_uses': 1954,
        'new_objects': 295, 'base_referenced_members': 253, 'logical_listing_sha256': LOGICAL_LIST_SHA,
        'explicit_empty_directory': EMPTY_DIR, 'green217_files': 217, 'red217_files': 217, 'baseline216_files': 216,
        'repeated_source_copies': 1770, 'durable_prior_corpus_copies': 78, 'accepted_review_method_files': 97,
        'all_restored_file_mode': '0600', 'all_restored_directory_mode': '0700', 'all_output_bytes_read_back': True, 'all_input_bytes_rechecked': True,
        'accepted_historical_observations': {'focused_red_each': {'nodes': 22, 'failed': 13, 'passed': 9}, 'focused_green_each': {'nodes': 46, 'passed': 46}, 'ordinary_sa21': {'passed': 2654, 'failed': 7}, 'ordinary_sa20': {'passed': 2608, 'failed': 7, 'skipped': 46}, 'optional38': {'passed': 38}},
        'evidence_claim': 'Preserved accepted byte evidence only; no fresh runtime or new supplemental linkage reconciliation claimed.',
        'reviewed_archived_synthetic_fixtures': 'Remain archived and labeled by preserved accepted bounded input-review dispositions; matched values not printed and no new secret scan.',
        'focused_synthetic_fixture_disposition_sha256': '640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022',
        'nested_packaging_distinct_bodies': 4, 'nested_packaging_bodies': 'Opaque; not decompressed, executed or used to recreate extracted47.',
        'historical_seven_failures': 'Unresolved prior disposition preserved', 'all_seven_gates': 'UNKNOWN',
        'live_source_reads': 0, 'archive_code_execution': False, 'raw_phase_secret_environment_cache_reads': False,
        'runtime_dependency_database_restore': False, 'product_import_test_build_install_database_server_network_git_operations': False,
        'qualification_nonclaims': ['No installed qualification', 'No fresh-host or independent-builder product reproducibility', 'No physical-release guarantee', 'No runtime environment', 'No release or production approval'],
    }
    report_raw = json_bytes(report)
    write_new('RESTORE_VERIFICATION.json', report_raw)
    expected['RESTORE_VERIFICATION.json'] = report_raw
    verify_tree(expected, empty)
    # Recheck fixed inputs again after the final report/output closure pass.
    for path, raw in snapshots.items():
        require(read_regular(path, len(raw)) == raw, 'Authenticated input drift after completion receipt')
    require(directory_entries(PARTS) == wanted, 'Additive readback closure drift after receipt')
    print(json.dumps({'status': report['status'], 'report': str(OUT / 'RESTORE_VERIFICATION.json'), 'logical_files': 2386, 'source_files': 217}, sort_keys=True))


if __name__ == '__main__':
    main()
