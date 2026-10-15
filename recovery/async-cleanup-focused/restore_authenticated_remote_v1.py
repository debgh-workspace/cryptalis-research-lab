"""DO NOT EXECUTE BEFORE INDEPENDENT REVIEW AND ACTUAL REMOTE AUTHENTICATION.

Offline, standard-library-only, pinned data restore. Authentication is supplied by
the coordinator's independently pinned receipt of actual authenticated remote
readbacks at one immutable commit. This program cannot authenticate a network
service and local staging must never be relabeled as remote readbacks.
No archive code, product import, test, dependency, environment, credential, Git,
network, subprocess, database, or server operation is performed.
Run only after separate execution authorization, using python -I -S and the two
independently established --expected-remote-commit and
--authenticated-provenance-sha256 arguments. See README.md for the trust boundary.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import lzma
import os
import re
import stat

P = Path('/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013')
PARTS = P / 'async-cleanup-focused-remote-parts'
OUTARCHIVE = P / 'async-cleanup-focused-remote-reconstructed.tar.xz'
OUTROOT = P / 'async-cleanup-focused-remote-fresh-extraction'
OUTSOURCE = P / 'async-cleanup-focused-remote-full217source'
OUTREPORT = P / 'async-cleanup-focused-remote-restore-verification.json'
REPOSITORY = 'debgh-workspace/cryptalis-research-lab'
REMOTE_PREFIX = 'recovery/async-cleanup-focused/parts'
ARCHIVE_NAME = 'CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz'
ARCHIVE_ROOT = 'CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1'
ARCHIVE_SHA256 = '1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af'
ARCHIVE_BYTES = 1029680
TAR_BYTES = 9543680
TOTAL_MEMBER_BYTES = 9148868
MAX_MEMBER_BYTES = 1746649
MEMBERS = 516
SOURCE_COUNT = 217
SOURCE_BYTES = 4423405
MANIFEST_NAME = 'FROZEN_PAYLOAD_MANIFEST-v1.json'
MANIFEST_SHA256 = 'e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174'
MANIFEST_BYTES = 95250
ALLOWLIST_NAME = 'freeze/FREEZE_CONTROL_ALLOWLIST-v1.json'
ALLOWLIST_SHA256 = '8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176'
INDEPENDENT_REVIEW_SHA256 = 'cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a'
INDEPENDENT_REVIEW_PATH = 'reviewer-notes/async-cleanup-frozen-independent-20261015/review.md'
FORBIDDEN_LEAVES = {'tests.json', 'rawtests.json', 'readiness.json', 'package-origin.json', 'postgres-start.json', 'postgres-stop.json'}
FORBIDDEN_PARTS = {'.git', '.venv', 'venv', 'env', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'node_modules', 'site-packages', 'runtime', 'source-repository', 'external-sources', '.ssh', '.aws', '.codex', 'credentials', 'secrets', 'environment', 'dependencies', 'cache', 'toolchain', 'pgdata', 'postgres-data'}

# Immutable preparation-generated pins. These are review data, never paths to
# follow in the live candidate or external runtime. Every archive member is here.
PART_MANIFEST_SHA256 = '95283f84eebc99775c574a6c2bc6c832c20bd9cedbe0edffdc5f4109adb24ca8'
PART_MANIFEST_BYTES = 2964
PART_MANIFEST_GIT_BLOB = '7c12ae61f986c0a8b81e135fe9ce60c7f13253ef'
EXPECTED_PARTS = [('part-01.bin',
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
EXPECTED_REMOTE_FILES = [('MANIFEST.json',
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
EXPECTED_PART_MANIFEST = {'archive': 'CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz',
 'archive_sha256': '1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af',
 'bytes': 1029680,
 'format': 'async-cleanup-focused-parts-v1',
 'independent_archive_review_sha256': 'cedb958ec9a873b49d8d6baa96bc55c348cd076d4840fd54fda3b22dc09d983a',
 'intended_remote_prefix': 'recovery/async-cleanup-focused/parts',
 'intended_repository': 'debgh-workspace/cryptalis-research-lab',
 'parts': [{'bytes': 96000,
            'git_blob_sha': '0dcab85978256326c767d5a3e457645f5f0a4f18',
            'name': 'part-01.bin',
            'sha256': 'b51274be79d8eff24dc5721bd6a87d77aa52072f834c205a9115638f2822397a'},
           {'bytes': 96000,
            'git_blob_sha': '785e2a7b50426c0f27bef562828faf9f3683ba97',
            'name': 'part-02.bin',
            'sha256': '929aa55505f8838316e20b45cfd39ff60d4fd8cbfc4633d915d8348dd2d3dfe3'},
           {'bytes': 96000,
            'git_blob_sha': '44a0764e78421fded21781a2258370f65f5c2dfa',
            'name': 'part-03.bin',
            'sha256': '168e6df70da63ec21ec1f196a81a8e526e87da4b76d86b624da39e21922e7d15'},
           {'bytes': 96000,
            'git_blob_sha': '0dfc10f58e27864e14f2c4aad8cc2909589ad237',
            'name': 'part-04.bin',
            'sha256': 'eb2f5efeea31f82742e99b970f44ff47c42a1d100e83d093778ba01ccdaf8a80'},
           {'bytes': 96000,
            'git_blob_sha': '3eb877ad43417c7d70a7fcc344cd4ad250d34dd9',
            'name': 'part-05.bin',
            'sha256': '017298da0170094ae3beb1d66bb110c04107f2b49eb769bab30ce48b40c22898'},
           {'bytes': 96000,
            'git_blob_sha': 'f05d199956353a71cb47d13dbcf6fded0b2d3240',
            'name': 'part-06.bin',
            'sha256': '8502cecb4d85a5e503000482609f095b61fab6d5e525ddf5ce7c1e0ecfa22a6e'},
           {'bytes': 96000,
            'git_blob_sha': 'c2b7807cd7e37d223bced1528eb76e801421f705',
            'name': 'part-07.bin',
            'sha256': '91208c5da9e232fbfb66fbe77b5b667c50fcdd84983b09b5dcc038cd7ad1d07b'},
           {'bytes': 96000,
            'git_blob_sha': '9da15ff11979148c592cdb466a405506624ec32f',
            'name': 'part-08.bin',
            'sha256': 'd5aeefbdb45a8c73b3313954c24926b4e85c79b6eefc6613067762f074747628'},
           {'bytes': 96000,
            'git_blob_sha': '45c8a5bc2c0c10a9828ed21c74f5dfc4fbaf100a',
            'name': 'part-09.bin',
            'sha256': '79fd6007c478c3d4d5961aae280442b82089bcf083a5325857406721b31c8174'},
           {'bytes': 96000,
            'git_blob_sha': 'd783c64af462a46262e94677d5328b2de24bbd1d',
            'name': 'part-10.bin',
            'sha256': '826a9b32b442d066e731d3ae075d4c03f915326476a5a5025e878b82d4e08e29'},
           {'bytes': 69680,
            'git_blob_sha': 'e9133e032d78b18107de18de23cd6b353fc3ed65',
            'name': 'part-11.bin',
            'sha256': 'b31cfc7364dc33639437364f52903cd3232f0697af06bd0522b750a02b91b37c'}],
 'scope': 'Accepted full217source and focused cleanup evidence data-only capsule; local parts are not authenticated '
          'remote readbacks.'}
EXPECTED_MEMBERS = {'FREEZE_ADDENDUM-v1.md': (2484, '095bf19789550f70b8cd13964e176812a15a8a21145700a69f6b310df37a6fbe'),
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
 'evidence/next-correctness-green-sa20-20261014/junit.xml': (8084, 'ce16756d212f6bbde75e2b748b995d3d5dacd0cf62538da3d6fd111969ab98c0'),
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
 'evidence/next-correctness-green-sa20-20261014/readiness.log': (46, '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-green-sa20-20261014/runner-receipt.json': (29509,
                                                                       '3a4cc09f74c48f2d1039dbc9626b9fe565c65b87c5c0367d3e22d59696fff368'),
 'evidence/next-correctness-green-sa20-20261014/source-before.json': (16955,
                                                                      '55f42dc25592c28a5d2313d5fcb733836b663491523c7fed5d0d1fa086ee5aea'),
 'evidence/next-correctness-green-sa20-20261014/source-root.json': (183,
                                                                    '2644bc2bb01b255fc4b8c79bf24a090c9e9d5f2fd5ec72aa59d9e19879837019'),
 'evidence/next-correctness-green-sa20-20261014/source-stability.json': (34587,
                                                                         'da522982915ef7c30e4188a315ee726eb270cff482a26f967b320e5ea20eda62'),
 'evidence/next-correctness-green-sa20-20261014/tests.log': (145, '3209b3b1ea81a9646875eefbc823dc8770b73ab600c099e4ebc51d1b27b3bf42'),
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
 'evidence/next-correctness-green-sa21-20261014/junit.xml': (8084, '5c3b2b4df8344725178a7196ba49344cad0e097232b1ae187f935d78c904c0a8'),
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
 'evidence/next-correctness-green-sa21-20261014/readiness.log': (46, '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-green-sa21-20261014/runner-receipt.json': (29508,
                                                                       '585ce3639c165fa390521cee8607e87dea2b831572e191e9d415e6943f955c6d'),
 'evidence/next-correctness-green-sa21-20261014/source-before.json': (16955,
                                                                      '55f42dc25592c28a5d2313d5fcb733836b663491523c7fed5d0d1fa086ee5aea'),
 'evidence/next-correctness-green-sa21-20261014/source-root.json': (183,
                                                                    '2644bc2bb01b255fc4b8c79bf24a090c9e9d5f2fd5ec72aa59d9e19879837019'),
 'evidence/next-correctness-green-sa21-20261014/source-stability.json': (34587,
                                                                         'da522982915ef7c30e4188a315ee726eb270cff482a26f967b320e5ea20eda62'),
 'evidence/next-correctness-green-sa21-20261014/tests.log': (145, 'dc792aa3ab23850999b9622e5b9a393d4eb476224161d245c3bc7c07d2cbd26a'),
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
 'evidence/next-correctness-red-sa20-20261014/junit.xml': (24410, 'ddf480207308914bc864191d6cfbbdace56b8380b7509f332dd5690d5e004de1'),
 'evidence/next-correctness-red-sa20-20261014/package-origin.log': (298,
                                                                    '7ba8a5c83ad7ccf0ba4f4c263c75879e92294b6c023551ff48e5bdeeb1da7d93'),
 'evidence/next-correctness-red-sa20-20261014/postgres-start.log': (52, '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-red-sa20-20261014/postgres-stop.log': (56, 'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
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
 'evidence/next-correctness-red-sa20-20261014/progress.jsonl': (22513, '1c160eef8bd87c1cdc67e8620e58afb3f32b4690c1c6dc75efbb9f657c18f01b'),
 'evidence/next-correctness-red-sa20-20261014/readiness.log': (46, '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-red-sa20-20261014/runner-receipt.json': (23810,
                                                                     '979a2f1484a0998ca1b1d54287217bd7cc99f6f71726ede098790cd3ac2ae4c4'),
 'evidence/next-correctness-red-sa20-20261014/source-before.json': (16955,
                                                                    'b6012d6e720458563a19fb8cc9337147808d122b941bbd98688ad774fa92e148'),
 'evidence/next-correctness-red-sa20-20261014/source-root.json': (187, '7b9d408e75e3c14a86661c7b8650b9f0520b002a5425ea9528d529b6dd203e8a'),
 'evidence/next-correctness-red-sa20-20261014/source-stability.json': (34587,
                                                                       '38d864add1d8e41fb57add6eb4cc772bbdb96fb29845be282225760f52c1ef21'),
 'evidence/next-correctness-red-sa20-20261014/tests.log': (18755, '584c083c9482a3ab51ba2c06e465212b9b8d3d67daf914b10a67189b64e52fda'),
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
 'evidence/next-correctness-red-sa21-20261014/junit.xml': (24410, 'dc2f42ac693296d353a2ab525e1e0b24e1c17b87322377574a2c85ca21cf9be0'),
 'evidence/next-correctness-red-sa21-20261014/package-origin.log': (298,
                                                                    '7ba8a5c83ad7ccf0ba4f4c263c75879e92294b6c023551ff48e5bdeeb1da7d93'),
 'evidence/next-correctness-red-sa21-20261014/postgres-start.log': (52, '66afd0411ccc09366e99fdd99b85f21899c8d2d064f5835126859618802153ad'),
 'evidence/next-correctness-red-sa21-20261014/postgres-stop.log': (56, 'ca19178a35ab4153b75b494963b66ce8243e1b94c173107c87b44d09db23652d'),
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
 'evidence/next-correctness-red-sa21-20261014/progress.jsonl': (22516, 'a2d085a7deee0e1b77debedd6a0096d3973655563c2601ea00cdcb74c527022d'),
 'evidence/next-correctness-red-sa21-20261014/readiness.log': (46, '650259218ffbeb1cdade25d6157c232eed7feb35be43a79af4d6d836ca9ddd08'),
 'evidence/next-correctness-red-sa21-20261014/runner-receipt.json': (23809,
                                                                     '441f0679bfe28c96152d5167652128ec4734b5e4f381c51e8d0f4f800c994c44'),
 'evidence/next-correctness-red-sa21-20261014/source-before.json': (16955,
                                                                    'b6012d6e720458563a19fb8cc9337147808d122b941bbd98688ad774fa92e148'),
 'evidence/next-correctness-red-sa21-20261014/source-root.json': (187, '7b9d408e75e3c14a86661c7b8650b9f0520b002a5425ea9528d529b6dd203e8a'),
 'evidence/next-correctness-red-sa21-20261014/source-stability.json': (34587,
                                                                       '38d864add1d8e41fb57add6eb4cc772bbdb96fb29845be282225760f52c1ef21'),
 'evidence/next-correctness-red-sa21-20261014/tests.log': (18755, '7e34bb558a8e69ab09105feb66af00154b02eb9715a0de8f8cf88b6804d81a62'),
 'experiments/next-unblocked-correctness-20261014/BASELINE_SOURCE_MANIFEST.json': (24182,
                                                                                   '3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703'),
 'experiments/next-unblocked-correctness-20261014/BASELINE_sqlalchemy.py': (63625,
                                                                            'df8ee448ed7bab52e5e1ecd61f5cd859464d4607fbac13b3ac62c2def4a5ece9'),
 'experiments/next-unblocked-correctness-20261014/FINDING.md': (4329, '6fa7b4532ef1bd1466976177b4124eca0efef578541fcaca808f06582372b538'),
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
 'experiments/next-unblocked-correctness-20261014/PLAN.md': (4866, 'eee951b1b7a5033e7b4d5c607afb6001fafe944c80ca29025af98782c67d9fcb'),
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
 'freeze/independent-review/REVIEW_ARTIFACTS.sha256': (789, '086bc51c5c374575be2d02ae0583bdf08e90a35e2239e43039509c6bcb86e3a5'),
 'freeze/independent-review/VALIDATED_INPUTS.json': (111996, '1f6e334bf6531c1004518f1171ce70fdb1836bc93f4e90588f51967ca92c25fb'),
 'freeze/independent-review/audit-summary.json': (4075, '7641e39d5bf45f9b1fd57eaf466b846e7dc0c0c52349fd2d03b9f74e6bf5485f'),
 'freeze/independent-review/audit_inputs.py': (22371, '0d40992126616a03626ac36954554f1d246f9322ce5a2afed1960c41f8c9790c'),
 'freeze/independent-review/checked-inputs.json': (167541, 'e13d3f4c3825a99f3b026d5433ca08ab460c8c972cc5700b9444802b223dbc8a'),
 'freeze/independent-review/filename-validation.json': (830, '86807914a89a2f4eff4e291bff314faa933bb68ee18a7cc15525e9d342bd6374'),
 'freeze/independent-review/node-reconciliation.json': (23653, 'cc2cf376d831364674d26c539646955a4f1c3a3c86549449d878722eb06e219d'),
 'freeze/independent-review/review.md': (5412, '5e8b065421a1f50c185f8c00f9f5be40070acacbfa8e05798cd43dc8f9bf5e63'),
 'freeze/independent-review/secret-pattern-dispositions.json': (1079, '640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022'),
 'freeze/independent-review/secret-pattern-scan.json': (689, 'c6b662e5b139bd591720783a3b8194679c6ca0edc9069f6aa150a4099b00e14b'),
 'freeze/independent_rebuild_restore.py': (13774, 'd4c17c7662c220434c889f8b8d3c38c60f1f57a7809ffaad9c44a628b841fe03'),
 'freeze/preparation/ALLOWLIST_SUMMARY.json': (585, '3996cc376bc83b6e928f7866625f247e37fbc29138bdf05076a2b2095fc54f5f'),
 'freeze/preparation/COPY_ALLOWLIST.json': (117133, '442857ea6560e7600566eee05823f968d58e9c2df0feccb98f05af82e3dce173'),
 'freeze/preparation/COPY_RESULT.json': (432, '3abfd4801f10f094b1843665c2bc61286ff821218988e2699960a968bf01f0d1'),
 'freeze/preparation/EXCLUDED_CACHE_DIRECTORIES.txt': (131, 'd61ec4bcca47dcfcf6ac25ffee4bca7c247c7fc3e4b1141f041927af49f94dd2'),
 'freeze/preparation/GENERATED_FILES.json': (657, '032b08923134a6fe9d4567446db78d156333faeab0fa197bd4fdee9bf5b1d9ef'),
 'freeze/preparation/PREPARATION_REVIEW.md': (3462, 'a30588daa563ef72987b0d017c14d64a68b1766574368d15ee4635e66279a189'),
 'freeze/preparation/PREPARED_CANDIDATE.sha256': (63968, 'aaec85c083fa001754b488dd89196db5d303c7b464f80eb13a4cd9f5ab344a6e'),
 'freeze/preparation/PREPARED_INPUTS.json': (167605, 'aadaf38be9c80103fbdf90f736491fbe928a1acb918180c1d2100a0f3aacafc7'),
 'freeze/preparation/PREPARED_PAYLOAD.sha256': (63808, 'e9486b5a85f2b7e287bd57791c53901fded78eed35f0dd2b241587112fbd8aae'),
 'freeze/preparation/PREPARER_DATA_CHECKS.json': (3597, 'f612589c82d8ed64e125988659d456830c66874a41f5eab540a2c3091d75ea23'),
 'freeze/preparation/SOURCE_FILENAME_ALLOWLIST.txt': (7764, 'a20f6dffc27545837d8399f390263057141df5690dc84ebf219367747ff17148'),
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
 'source/docs/research/CRYPTALIS_FINAL_REVAMP_BLUEPRINT.md': (1746649, 'ceb2fa7376b169dff636e678977139b7b1dd9f63c2c45e0d7ec98a22d261228e'),
 'source/docs/research/CURRENT_COMPATIBILITY_CORPUS_20261012.json': (222039,
                                                                     '9df455d63a89a0cb1cc4e6ee22bfdd0e3b50c2899187265bf3a8081bccebe971'),
 'source/docs/research/CURRENT_VERIFIED_CHECKPOINT.md': (18743, 'e3e981b4f524a463b33468be59bce153608b843bad2e72d4f13bab79198702a7'),
 'source/docs/research/DEFECT_REGISTER_20261012.md': (25765, 'ab13363966b0f5979747e435c77cdc8f8ecfc6d630062155a2bd2b3a4441b0ba'),
 'source/docs/research/DELETE_TEMPORAL_CHECKPOINT_20261012.md': (2762, '578bfbceb86a25318021e464d28e16f026f50ab3a1cacdd1103ae8435f57dc0b'),
 'source/docs/research/DX_ENGINE_PREFLIGHT_20261013.md': (3400, '913a9b42b39646f80c0c55f37b47c57f323d988a75a94f065f45d6ce7a7259c3'),
 'source/docs/research/INPLACE_LAYOUT_RESEARCH_20261012.md': (3948, '89c1488ab138dee26dc0d0f119d3702324caf3df9d1522428cc240c3653c5617'),
 'source/docs/research/LAYOUT_COST_AND_COMPETING_DESIGNS_20261012.md': (4792,
                                                                        'ae082e67192f7474a6d31c05ad3db235a31f21b1ea1c22e2b1d1a0b4241f9bdf'),
 'source/docs/research/MANIFEST_SETUP_20261013.md': (6925, '1dca76e91c8fb5bf3a152ec56cda558a92276a58ad96366b3ba3a2398c96a118'),
 'source/docs/research/NATIVE_DELETE_CHECKPOINT_20261012.md': (2462, '148884ffd9f2eaf129b87c2187f7f1d41b09e851c6cb3e785b4a291d1a89f9c6'),
 'source/docs/research/NOT_INCLUDED_20261012.md': (560, 'bbb01253517840afc087ed2494e3186865af2fa1a725392cdf9b9d28f766aeac'),
 'source/docs/research/PRIVATE_PUBLIC_UPDATE_20261013.md': (10090, 'a182472b08d9bf696079a052773455df1010a6ec9cd47ce629812c2cda8c52a3'),
 'source/docs/research/README.md': (1228, 'f47b5570ecd76c324f01d7805d813381dbc3b05a2243c4bd8845222f67678cd6'),
 'source/docs/research/RESEARCH_CANDIDATES.md': (1757, '898819b846380bf148ea8e739f605b28ea9d958b51434ba1259e75b37153f5c4'),
 'source/docs/research/SEARCHABLE_REVERSIBLE_CHECKPOINT_20261012.md': (5765,
                                                                       '460b6f0b0e3e4aed058b3ec5e763ec21f96b5c0b644b6350a6794fac5e2a0e8b'),
 'source/docs/research/TEXTUAL_REFERENCE_REFUSAL_CHECKPOINT_20261013.md': (4530,
                                                                           'a2d489e8f00b904a0560ae329b7225de8dd7cd9566905d472253d69d1b72f0e3'),
 'source/docs/research/council-review-1/report.md': (17846, 'dace62c1a3036095a14570b2e0430901aa28b8300eaa135e4b90f2d475b6a641'),
 'source/docs/research/council-review-2/report.md': (5403, '3dbe2be24e18cdbb5f97f5e88568f791daa5e10a9171089a23121b592e7479f2'),
 'source/docs/research/council-review-2/work-ledger.md': (7206, '09c8b885fa6c6e3426205f2bb176b417168c0908aae08d547c89fd7e3b4dde4c'),
 'source/docs/research/cryptographer-review-packet.md': (42514, '8f9a21f08082ce595fe75c648ed91aa5ddd8ad306893a44cf5dd7758da2e8f73'),
 'source/docs/research/hardening-evidence.md': (6809, 'e9d163caa8ced42c75893f59815a2a30b823f00c8525b6fa2ccfc2794b540733'),
 'source/docs/research/hardening-resolution.md': (17131, '27b5e3d554f99596defb29e9fbc40858e74f0429d14d6964a8161cdbbda24fba'),
 'source/docs/research/performance-checkpoint.md': (18200, 'bd55fcd474ff411a8708510fe260c174bc2a1c9d5381bd17f24d836fed43f0bd'),
 'source/docs/research/reset-crypto-authority-evidence.md': (22505, '3413219dfd2e3e439fb4cbc2d25e6585f853f3c3d3463370e0020f713cb5a772'),
 'source/docs/research/reset-integration-search-evidence.md': (36262, '5f7a3f44c28e3401eaa652c1edd6a05bd86f726e10f81b6eddca2a936eff9d90'),
 'source/docs/research/reset-leakage-semantics-evidence.md': (8554, '44519fde2adbc643562e58ac7b58784e904e57dca8507f34ce72b922beb5b54c'),
 'source/docs/research/reset-operations-release-evidence.md': (24436, 'b888bb61657044ac8ff7a91740c09c6a26c6317a78a1683506ec56843747c4ca'),
 'source/docs/research/reset-traceability.md': (131467, '07905f69e676e1bed111375d474b1c5d8e5e72f8831bad986bcf8586b9b6e823'),
 'source/docs/research/revamp-evidence.md': (48163, '815761e3cca9d18aef254bd25d543d381f51fc54e18258c1e7a0f21914811c73'),
 'source/docs/security.md': (31672, '27546dd4022c4a3353066bec05dee76e97cda8a4f1e16e26b656e7572b0abc45'),
 'source/docs/status.md': (68283, '31d35e60db1de7ab2a6939d0c061118e6cee9000f0705c943209ca7086fcddbb'),
 'source/docs/walkthrough-migration.md': (4330, '31fe61df71acfaefd8570b1438ea0a5a13a1805dc8f88c8bc5aca3b97db964d0'),
 'source/docs/walkthrough-search.md': (2882, 'f2bfebbd07c80b511207b1d746136fde05224a0f8cc9239018d296c8efc5af05'),
 'source/docs/walkthrough-sqlalchemy.md': (2911, 'de07d118889fa01b674aec8cb909e69da7f1edb2c77be577da2f4f1bd5ca96d3'),
 'source/examples/active-state/genesis.json': (395, 'f4a1e408b6303cb9dc4cb094770d49346609790a0ee5e00337e1b5afe8b14763'),
 'source/examples/active-state/successor.json': (491, 'aea1f6f6b022d390f9a8fc68cad482d7c4df47b14e602076d354b7834f4635ab'),
 'source/examples/demo_manifest_history.py': (4344, 'bad9d66bbb99ab788286ccbe10f4215d3c1eec73d6f4124d8c1d2672ad5df628'),
 'source/examples/demo_smolink_crypto.py': (12461, '9197d05f04937e14ce317245c97aa9d5d7e3777c4c13a49b01bb621ca114a4a6'),
 'source/examples/envelopes/f1-structural.hex': (291, '60effcfdfced026cadf09afa94ee7d300f178693b61136adfa9186019a6c8bb9'),
 'source/examples/envelopes/w1-structural.hex': (319, 'd7eda7903401ce52bc67cbc01c3bd3bd02ac05b78d1ffaef66743c4eb04440c9'),
 'source/examples/field-formats/parameterless.json': (454, 'f5a0a56b8b7332a99fcff8a48314fff3241592c1f521b2c6681653326e2c13b1'),
 'source/examples/manifests/genesis.json': (125, 'ab9fb3baa09924c883940c926b2406c3e6604e93b95eb1cc024cc89f51fa24a2'),
 'source/examples/manifests/invalid-duplicate.json': (184, '6e82f332c08ad8ad1ab8355c190c77210ec94e15b27d21b5b1029cbff4e4b970'),
 'source/examples/manifests/invalid-successor.json': (167, '7facec7579d006cbd50f71e42a24675c1640685ac03e0d5f159f45da497771d6'),
 'source/examples/manifests/successor.json': (187, '2e9881b401babc7238764df0ac5ee108b4e14c0d9935727ca419b5edcfd821bd'),
 'source/examples/scalars/candidate-vectors.json': (1003, '8028c66f120118c3bf0de9f93aeeca23da5c5893624b44c5a16a52e74ca33be9'),
 'source/experiments/manifest_setup_fastapi_models.py': (5788, '220f4640722c520948afd7db4179f8c4c815eb51da4ae71cca73a4a0d7fa51aa'),
 'source/pyproject.toml': (552, '4653756dfe6a3dd1a185f636efb1ea0135b5235d9cdc138f30667d1f0975487f'),
 'source/scripts/test_postgres.py': (6071, '118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12'),
 'source/src/cryptalis/__init__.py': (36, 'c1a82f9f958187e4b5423d11df5a035b17d75b34a0947af6be4aac436cd2fed2'),
 'source/src/cryptalis/__main__.py': (58, '9967032819ce6f18e02a40d033958d5f4f7c328faf8693bc07ecc42a1a525707'),
 'source/src/cryptalis/_doctor_ciphertext.py': (4359, '42e9424fbe55e982463032668a9365bed2c796714ff17649da2adf725fa6e755'),
 'source/src/cryptalis/_doctor_setup.py': (10364, '6637ff4aee2b4ac27628d56ea9b73ad5e2380782eebc0bba23192c3eff1583e6'),
 'source/src/cryptalis/_experimental_public_delete.py': (18468, '074c0e41cd728ec5e59bb20665b22bc2a2cf6d1b51d5b5dcca0b8ee262126270'),
 'source/src/cryptalis/_experimental_public_update.py': (10285, 'bfd2e84e30acab549f7b221110b7bec3aa150bc16084669ea32a462a4e8c20c3'),
 'source/src/cryptalis/_native_text.py': (2237, '39460e5f75f72b15c8f98c5b4c333a18a432668990f31bc80f0c6887c1bbd170'),
 'source/src/cryptalis/_object_comments.py': (12999, '00c6bc68768fffc813bdfa4ee5302e93d4f76a9754b7b704955cf186c978192c'),
 'source/src/cryptalis/_sqlalchemy_guard.py': (4807, 'e4dfb340fadb36ba2544267e714e2414c465bf64313ae6b27c058d1da4c7f819'),
 'source/src/cryptalis/_sqlalchemy_search.py': (9557, '857bb89d2f0aae0dc8b41f7c14bcc9dcd5285640fbe0969fbd8421ef2059ee63'),
 'source/src/cryptalis/_sqlalchemy_transactions.py': (8273, 'cb128481811576d8f16b233d4a30fca060eb9a1bfc4459d5e7e129434cc522ec'),
 'source/src/cryptalis/_sqlmodel_support.py': (2566, 'c3b30313e0078bf39b16eef15802fb412d5f5ac9dc10938fa4c311fcb9ac449d'),
 'source/src/cryptalis/_transition_json.py': (2150, '2110f79fc1f38500daaaa2da814224afda9a9a92a5e8e776420d9168736d8a19'),
 'source/src/cryptalis/cli.py': (17882, '0df0b4f0101933b3a069024965b7bc5a3374747aff53d37099d2f22efc105efe'),
 'source/src/cryptalis/contracts/__init__.py': (58, '7a621ddfa3ed2dd543a3495b8cedaed3f892fc6b1fae0b6e8d04285741bd8660'),
 'source/src/cryptalis/contracts/active_state.py': (8925, 'b22608114fda5f49b2fa054fef24763bc9735c37612edfce0b13e16ca0df7532'),
 'source/src/cryptalis/contracts/development_authority.py': (3337, '1fe8519fe06fd0121829b92e04f1b5be2b8b72e39f3b8eecc3d60b6e168810d7'),
 'source/src/cryptalis/contracts/transition.py': (6485, '407c8028827ac7660cf6c4d3d4cfae30ca2dacf69ca80749e4e52f07d5c3d923'),
 'source/src/cryptalis/crypto/__init__.py': (961, '15ab27443d10863330631cf53c48e5643934919e470f9e2138db7f59434befc2'),
 'source/src/cryptalis/crypto/_candidate_envelope.py': (3964, '9c28cb84a85123130328b2273eb27786a95f7953a41f0ec27f1c11100e28e55f'),
 'source/src/cryptalis/crypto/_candidate_scalar.py': (7050, 'b97a21a29b4bc9453af8c4c0a8f22b4860892b85854b5d1196ebca2f5094269a'),
 'source/src/cryptalis/crypto/_candidate_wrap.py': (3518, '18cd89777178a5938848c51d47b48603dab902f57e83a6b330a8643f92748dc4'),
 'source/src/cryptalis/crypto/_payload_rotation.py': (5027, 'eb1117e9f03710bcd04d4139c181930102573c5f3de7f9167a7178c2660c295e'),
 'source/src/cryptalis/crypto/_rewrap.py': (2708, '797d1789c983e8c4eba36a792c8d4b5c00cba734bd25b61d6a970f1711be734b'),
 'source/src/cryptalis/crypto/cf1.py': (9977, 'd74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278'),
 'source/src/cryptalis/crypto/development_file.py': (5207, '12e3ace1bf41a551c3ce98719c1b6f06aa004125afb79f72eed1e746f6b858a4'),
 'source/src/cryptalis/crypto/keys.py': (14233, 'b76d60f32011705726cc73f6211fa52e5624e475fc63573e578aa9e5078aea56'),
 'source/src/cryptalis/cutover.py': (12254, 'bef95a5d97b256ea1fa56565fcb9e1a1d2786748757777cf366b453d3cf42783'),
 'source/src/cryptalis/deprotection.py': (32239, 'f84a551eb27fe238ecaed3a21d468e243e31d20674b8965c5ac7ce421e04a16a'),
 'source/src/cryptalis/doctor.py': (11085, 'c2f4e7523ffe496bd8d0bac44d541c24bf532eea78e8cd42823014dae6875a72'),
 'source/src/cryptalis/manifest/__init__.py': (79, 'd2dc8653181d66161df9d9eb29ea79fb36b38fd93848d4da4a25184cda6885cd'),
 'source/src/cryptalis/manifest/canonical.py': (759, '6fe7e3d22cece14e5d85de912acdaf782a5421bfaa5c4dd796f78ab5bd4c2ec8'),
 'source/src/cryptalis/manifest/compatibility.py': (24725, 'ba8ce979234426f0e16961fa065fd54dda7bceb50c7019e2bc5e11b33d092920'),
 'source/src/cryptalis/manifest/compiler.py': (51172, 'dca174cba23517abfcb03e8a1df7ef12f9f7e1171b765e3c1b2da26edb23951b'),
 'source/src/cryptalis/manifest/declaration.py': (7156, 'ea4162c8686f46ad8fe1ffdd1500186c55a3f4eee861469e64de603dca79d35b'),
 'source/src/cryptalis/manifest/descriptor.py': (2984, '739d0438451c47746850c6aa488add4cfd7782ddeebd743741cccd290d2ce20d'),
 'source/src/cryptalis/manifest/header.py': (5449, '6e450d8565e3d7c19ecedd6c6b3120715ea5c7ee3b1ee439fef9e5080bb5eb6a'),
 'source/src/cryptalis/manifest/parser.py': (3380, '47cd75cc2ca611fe186d36d5d046317b0746714945c11fd2f84917d2f1020448'),
 'source/src/cryptalis/manifest/routines.py': (4219, 'aad088b76dc9f2a16604d80d1210d80b99e9efb691948b0392bfcd881f73c4b8'),
 'source/src/cryptalis/migration.py': (51082, '5db6aed86a8bab6576582eaace940aae4ca022ec79b744c55bc6be2c5a4d6967'),
 'source/src/cryptalis/sqlalchemy.py': (65537, '6a9b7b5a6bf2f16fe254134f228531188ab02dae16201e87c15a6537d07dfa30'),
 'source/tests/async_sqlmodel_oracle_support.py': (10075, '28a8eb13d10c5ea717cf2f88fd391c52f40cd834b2f2790bdb66f1da6404ab09'),
 'source/tests/conftest.py': (1584, 'fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd'),
 'source/tests/deprotection_native_worker.py': (1252, '4e8831ad2673a1a962dc1d4898ffe98aaa6d27becf990bbb81188015edea9d7d'),
 'source/tests/deprotection_worker.py': (1237, 'eb40b2c4c79834948cbf9799b05c901ff22ad516c146e3e18087ffb619756346'),
 'source/tests/fixtures/cf1_vectors.json': (28718, '24c918629ac10d7fb739fd02a946ecdbbcf1de4102bb353cf069cc095a3b286e'),
 'source/tests/migration_commit_proxy.py': (4660, '9d904aa020dac32413689e2b16d2dce06e654f07f16c969cc565fbdb385a6fbb'),
 'source/tests/migration_worker.py': (766, '033b592d725ec574bd430538046eae46a887b485309ed17bddcbbacb79558735'),
 'source/tests/profile_membership.py': (8138, '94ce19cc8df73876a099751b6cffd4a6bfabf40f9bf44192a1c6956955a1ad75'),
 'source/tests/profile_migration.py': (7680, '27180a224858a65a8b671e65541d710c76c488eedd7d61bf3902b3274c06ed81'),
 'source/tests/profile_migration_step_a.py': (15671, '69a5d7326184875f36004366df5f1db0cf1c780c49c82559835dc40490087cf7'),
 'source/tests/profile_sqlalchemy_adapter.py': (13895, 'e86690838c256d0e16b1ef498d154d3616f66960ca6a5215f01f61e734d2bed4'),
 'source/tests/profile_sqlalchemy_search.py': (20874, '19445c1ea169728af07630734d3c2dba8f5ece7679907899ff0105de16180692'),
 'source/tests/reference_cf1_vectors.py': (12714, '7be77c31e92ffb7255900b01e4b895ed40c935049ad2063c848492444c7e8e19'),
 'source/tests/regress_migration.py': (6793, 'b00267c6b1d507bc7cf66f983083c06b191d92e6c4f68dd618405f040d38e677'),
 'source/tests/regress_migration_corrective.py': (7994, '3729a3f2186faf16e655b271a1f9a74eee8e92c031af40bc97f56693d1a9828d'),
 'source/tests/regress_migration_lock_queue.py': (5474, 'f13556f0bc5f0636bc8ca5c0f11b519c3e0dbb9376437ca450a7643e8d1df6c6'),
 'source/tests/regress_migration_membership.py': (4054, 'c2bae8a71fea8f9e65f753e8d879c509611e0dad03f5ce38ebcd663e4c4790ca'),
 'source/tests/regress_migration_pause.py': (5590, '8d4b3b0a642e383bc1754d0369fecd7ee926283492b90e16be64d6fa4bb86cc8'),
 'source/tests/single_tenant_public_cascade_fixture.py': (4477, '346d4693e51a63a74e215cc3e823e094996066cbcb0f07a9eb2233fa091d48b7'),
 'source/tests/test_active_state.py': (10920, '6f57b46391a880b1c3dc2eeca8277baef3143eda7e99b56c05c95811c335b466'),
 'source/tests/test_adoption_diagnostic_currency.py': (2362, 'd2d744a6d48a71b4e094a9637b3d14f3dad134c23c38683783649248f8121011'),
 'source/tests/test_async_sqlmodel_public_hook.py': (35646, '1e3a49fe28ecf0d41ecf739ec260ff4378f5ab03c463615c90fa91771eb715b7'),
 'source/tests/test_attachment_engine_preflight.py': (5031, '118c49e0ef14b30ecd4d35e43c0458a33382c765e5610342b488b6d88756ef86'),
 'source/tests/test_candidate_envelope.py': (7572, '0719e40a1fd9ab123ea601d4c4177287101a8984efe282ee786200464628b860'),
 'source/tests/test_candidate_scalar.py': (14141, '7230944955a67c2ee91cf170b7ff2f280fc0c76bdfd56c97882d8110d5c277b5'),
 'source/tests/test_candidate_wrap.py': (6941, '85aa66f3e2ed625e20f13eedc1a41b38049c0ef4b9815928c878f9b943ba8457'),
 'source/tests/test_catalog_search_path.py': (9250, 'eae05b0f2bc1940ab382f47c499ad281de9972d44b67b7e3f2cc0554a8e184f0'),
 'source/tests/test_cf1.py': (23069, '911a67a9d98e8e61fb215e913b038d4dd820ba414cd14c1ec6f30e374044ecf2'),
 'source/tests/test_cf1_backend_failures.py': (4970, '960a3048895b4b4ce272630a5870f1443ab25a252e26dcb48dfb0a1366135a1e'),
 'source/tests/test_cli.py': (25921, 'd013dce84a813bdde34917a2778d1669bdd89e7960dd975f22905a2b5e8a0ca9'),
 'source/tests/test_cli_history.py': (10267, '44b0886c98b3031fa6e18499f456f162b69bd5424b4c7e88bc670d97af379df5'),
 'source/tests/test_compatibility_namedexpr.py': (3586, '05b69558fd5b72781f81f63c48ba1c46f6307f4b2f0cc0e6d653d7735dbb2eef'),
 'source/tests/test_compatibility_report.py': (9577, '1d220fa656af7d2120440572b60d7a2388ecac7c075dd8a59372f2722f62910b'),
 'source/tests/test_compatibility_statement_bindings.py': (6267, 'f5a20b9a49ce5dc0c36199d41a0811ef8115bdd5c58685052fe33b89dd787cbd'),
 'source/tests/test_compatibility_string_bindings.py': (6374, 'fea21ff5374d165112d4370514fbdd430f708db96635e0aea2d4f9aff22f1ed8'),
 'source/tests/test_database_diagnostics.py': (2183, '69c1faee437d1940edfb2a216ea5f350b7447fabda2286e20118fa09139fd4ff'),
 'source/tests/test_deprotection.py': (26710, 'a7bcc6d2c1dad5161f76a49e19c565481f78ebce2608af768f98b5deb1e93d32'),
 'source/tests/test_deprotection_ordinals.py': (5528, '4855458d1b0847c353accab010b8521cc7374601f272340df8b2367ea8ea9cd5'),
 'source/tests/test_development_authority.py': (5178, '7ec9747dd8e5f4c9bffe073a777f70388c3b2d8c9ca22b9c2d9af95d0c49ea80'),
 'source/tests/test_doctor.py': (6832, '8a546981a1d154fd39245cf5cdee773a64c6d191a2905aa18a84a459aa711f20'),
 'source/tests/test_doctor_active.py': (6724, '82765e928801c5f0f2c65ea43db94a6245d06679dc72260ebf356dfac2f8715a'),
 'source/tests/test_doctor_ciphertext.py': (7877, '172fc0e8ae2a8f3dbce44d5eff7648094ad53a5c6c3de4ea217459a1a43f4acb'),
 'source/tests/test_doctor_setup.py': (16410, '1f6c10d1e470dac43a352f436e98bc57bd3af9fd8e662a8dfc45875815f9d833'),
 'source/tests/test_doctor_snapshot.py': (4179, 'bc2749571dc2941878e53e6bb02c4e4f5b0b841480ed3df39f43c471771e29d2'),
 'source/tests/test_file_development_provider.py': (6449, '4d4e51ffb221a218fe6b1a91ce0d42ab65c5126d3ce8c746a1d4a36f43d57cc4'),
 'source/tests/test_file_provider_postgres.py': (3646, '7fc0923d2efcc57b1c351fb838fb2737651ba4e054c47fe6c9e6fd1c50fcca4a'),
 'source/tests/test_key_lease_renewal.py': (4441, '68fdae216597da746dc659ed8a0de0dfb30469094a9090a02d60fda10196e113'),
 'source/tests/test_maintenance_budget_boundary.py': (6567, 'ea8e48b6304887d65df72d0b0d0ad3ee99a4fd97bfabfa13aedc32693129ab81'),
 'source/tests/test_manifest_canonical.py': (8454, 'f95532844a798f986c44034096625eccd835a13d0df9c0c3befc0a3d5d4cc1e9'),
 'source/tests/test_manifest_header.py': (6564, 'd3d3724688f7ed790e35f253bce9cab77909f42819355e16f7a59e5e8b55cb8f'),
 'source/tests/test_manifest_parser.py': (5201, '3028e621d207b5e1435f504bada3a465720993c41681b7422978750de75dd0f7'),
 'source/tests/test_migration.py': (43808, '523cad2b77b760f01a52d8a7c96cb3005e56254af44be60e00b684d14ed8105c'),
 'source/tests/test_migration_audit.py': (12244, '77a275b649b1745bf5ecf02d2938098c1a3bb424917cac489bc63ef3ce93edc5'),
 'source/tests/test_migration_byte_bounds.py': (7040, '8eaebefa3df2fa06c752e3d2594065edbce0b46cb6cc370f86b7613dd81c92b7'),
 'source/tests/test_migration_fault_selector.py': (869, '7ee5265df9c66bd992d6ecec8fd878fa71a832ee7ec26db6286a4ce65f9883c8'),
 'source/tests/test_migration_key_leases.py': (5769, '574005b19b30d62e96fa2f536dbd645701ef996b1afca6339110a3aaafbef96d'),
 'source/tests/test_migration_lock_queue.py': (12013, 'da4a1f20a3b077900761124853121a348e930569198437b289d60ce26b693197'),
 'source/tests/test_migration_membership.py': (5004, 'a6ec0e602bbea264a1af29b6608a44e782aca7d7fac9a6835c58ea0766e6b623'),
 'source/tests/test_migration_multitable.py': (18962, 'bda36abba7f1aed88430b34f49dfab98657b2baffad19e29dc671922159b3891'),
 'source/tests/test_migration_pause.py': (8057, '870e8c9bb4a274cb1ba946d83e714227de527683d001d8e47345fac009ef6e8e'),
 'source/tests/test_migration_plan_diagnostics.py': (1457, '38e3b1aa5a3e2dc4b0978d3e01df0c29f53015c776dcbab6c6345766094ef0b6'),
 'source/tests/test_migration_role_template.py': (1200, 'c5229750cc28a970cafea1e4c769bddc0db07dfe5de46088618747598be0766f'),
 'source/tests/test_migration_runtime_privileges.py': (6916, '3fba8a3efb78ad2b1287a063ffa2da648738d3f010e205b10486cf8baeedf436'),
 'source/tests/test_migration_snapshot_boundary.py': (4138, 'ec0d5fa61fdc5e14e81763ad07b5cdd8581411e31602250069b228249df2487a'),
 'source/tests/test_payload_rotation_preparation.py': (18913, 'eb841213900dd279efbfcbc47c18c99e5fa714308f594f65e3aa335c71be481a'),
 'source/tests/test_plan_estimate_bounds.py': (3147, 'b9fb83970dc1fdeb65d07503bb6da278d5537b51e7da129516a6b792d809b47a'),
 'source/tests/test_plan_provider_snapshot.py': (8046, '58f9f1e5b2226944ba9dc10d23d4b250a9b49a1c49a6f601f86a9d8b3bf54802'),
 'source/tests/test_private_public_update.py': (23559, '44b03cbee5469cab0ac3b5dc7d5e870f2adf12aba73e89b3947f6a445e3b25a6'),
 'source/tests/test_private_public_update_faults.py': (26148, 'b02b835db801c7b0bc735323ea91e058ed8d2bc1e3408b39604ea1aa280281e6'),
 'source/tests/test_protection_compiler.py': (24656, '5ff497e6e052c33204cfe251313407304459467b2d5e5286269b817a38222587'),
 'source/tests/test_protection_declaration.py': (5546, '23e047858168d10d5788aaf5bcbd5af867e35cef2f8b4e035ed616b2015fdd38'),
 'source/tests/test_query_capability_survey.py': (7371, 'c87ef2c5b9fbc9e4dafb79ab77be5c275737e3a2c1764b7f1d1e431919a09f4a'),
 'source/tests/test_removal_input_diagnostics.py': (5549, 'f87f4afdb5d8b9971b71cbd0961a7f9c411f681a06bbb67c279354dd7fdd4fe3'),
 'source/tests/test_retained_profile_safety_oracles.py': (16240, 'e5467ca180f679abcedef5dc105690aa64912900cf43ee46c4935c715fddbfae'),
 'source/tests/test_retained_public_metadata.py': (6862, 'e55ed82ba4b9183c81bd24577fcf05f6ed123de86f3c9b46610dc914b4f424a9'),
 'source/tests/test_retained_schema_errors.py': (6527, 'ba7a4869e0017ca0b812bbe1025d0f325ba578e407f948b0a2803166a31fa215'),
 'source/tests/test_reverse_policy_drift_recovery.py': (8476, '22c0d97956346dd606abdf1de88e1d605917741868b3f0fe45aeeaa6f188eeb5'),
 'source/tests/test_reverse_predecessor_consistency.py': (9711, '1f90dae3613cd57bcb9817af6da2411e26134227b1c3681303b6dd46e8a1017d'),
 'source/tests/test_rewrap_preparation.py': (5058, 'd46556cc48301421c6bfeea7f7fa5624cf9f8bead9ae5e84ffaa5a2dd63b9a19'),
 'source/tests/test_routine_admission.py': (9056, '2fbc94ce31745497c5f52294e87d5b28cf2c9ea4859d9d55d1ab776d7e62ab01'),
 'source/tests/test_smolink_crypto_demo.py': (8843, '9410b81569287ab90534db2fac92edb932e7a38000e0a4caf0433ccb61a1ccb1'),
 'source/tests/test_sqlalchemy_adapter.py': (69975, '3f6deb6e0837596c0db6e8ebf19db19c042276bc091304e85766886184ef0c50'),
 'source/tests/test_sqlalchemy_async_cleanup.py': (7900, '19191d11b6c02774bb3b3ce449c09b526a87ddf1c8730eb3393578c58cd5e789'),
 'source/tests/test_sqlalchemy_async_collection_methods.py': (5802, '731278111ce02f66f18f15a5d6e17bd287607eaa019786718a4eb1099d6335be'),
 'source/tests/test_sqlalchemy_async_exit_double_failure.py': (17123, 'b01604d52da66697da025fe2d752b14700d304a3123408bb19b24c8863cf5978'),
 'source/tests/test_sqlalchemy_client_default_boundary.py': (16861, 'b12997edabab634c01c8b26f8f946392a70503d55389fa6cd826f979b33535e2'),
 'source/tests/test_sqlalchemy_core_autoflush_boundary.py': (4362, 'b27c4b2256db7595eafabb7477cdbd259b69a91e977bfa7b03a6848f3cb5cf4e'),
 'source/tests/test_sqlalchemy_flush_preparation_failure.py': (12508, '8e86b882cc1a41d3a0971fa0b4f58e696ccf9e5c9647ed0844e21168c2055ee0'),
 'source/tests/test_sqlalchemy_negative_predicates.py': (6461, '7578af71af7c774ad6c03d327d8bbe1f6fc5c605511b59062a4306667ff7fb20'),
 'source/tests/test_sqlalchemy_optimistic_versioning.py': (9865, '763ee88b0d01ea8e64cdcae9b3c55b5052a39ac4fe14f24492f06544e2a55d96'),
 'source/tests/test_sqlalchemy_ordering_labels.py': (7167, 'dcd8eba3c0f1c3315e28834b1b6d0674b36479f31cf6cd94ea6293e6b1b0a83f'),
 'source/tests/test_sqlalchemy_outer_nulls.py': (8057, '21a75523e968dde650f3082c08ca25d8355fbdd50cff7335ed33471fc3bc5abd'),
 'source/tests/test_sqlalchemy_provider_implicit_flush.py': (4229, '052ecfeba2d7df358433be89545222d73e7c8816fa09b667fe4ceec4e282a3a9'),
 'source/tests/test_sqlalchemy_provider_no_flush.py': (2643, '536f14671cb3c80e0f550464088cda73d6dc808985d292fc1c99a5073cf4a746'),
 'source/tests/test_sqlalchemy_savepoint_faults.py': (4966, '93f6d6ec618205eed0e0964054bd26a6e1eba594771b378ddf65edd99c2514ff'),
 'source/tests/test_sqlalchemy_savepoints.py': (12458, 'cf30f6d79d3e8b5b03bca7c0c777a9886754294cc5fe1ee617385d5922857977'),
 'source/tests/test_sqlalchemy_search.py': (65223, '0d9de8f210d482db210b982e0aa2b027e989e0deb589114a753ee4dfbf869015'),
 'source/tests/test_sqlalchemy_session_execution_options.py': (3944, 'fd07afde8c59159dcb888c2c67fc74a2030b9da4f77db915e51453fd1dc407e6'),
 'source/tests/test_sqlalchemy_thread_isolation.py': (3352, 'ab4137ee0a0b3e570b2a712d6c230bf14cdd03171bd5c5c2ddf4701fb900dfb3'),
 'source/tests/test_sqlalchemy_versioned_savepoints.py': (10095, 'fb5556204289e677b8b688af8ff28111ea8766477d99e8cd5482f54499efd143'),
 'source/tests/test_textual_clause_boundary.py': (7451, '68cad71a86f5d7471c32a3bdafa0da72ec751530f6b451a50412aa20e109f4fc'),
 'source/tests/test_textual_from_boundary.py': (6121, '43bf89c1e5030101c8d590db4a4c56fb1eb4b2514ee184a2b868f3eb9ec009bf'),
 'source/tests/test_textual_group_shadow_boundary.py': (946, '9ffbbc24c425d76b060ba22d3cf2d744df97bb2278728ea5adadc342e9611aa6'),
 'source/tests/test_transition.py': (6658, '54180b2df385b9fba43144bfab097d921e1b4510823ed7447be396c7aedf9f93'),
 'source/tests/test_transition_rate_estimates.py': (4518, '263ef93fdc5d03d54eb825056ec939c9757cfede399045b73248c923c5e4dfad'),
 'source/tests/test_tuple_encoding_oracle.py': (1133, 'c2081959dffa691828aba498beeb77398c6489c6ebc935b626de71758bb45b40'),
 'source/tests/test_unqualified_public_child.py': (7554, '5dca9ee725d581bffbfc07c93251eca9d954bc10a6ae1b8b3aac9d46d56d414b'),
 'source/tests/test_unqualified_public_child_async.py': (3142, '6fc0fa244d8f0beed24cad10b300bfbfbc69f582ecde58a314a97042db3132a5'),
 'source/tests/test_varchar_admission.py': (2003, 'f3ff42c473cd2c3a7202d9395a9feedfa9b595004b48298d19ecfb303e0cf3c7'),
 'source/tests/test_varchar_failure_boundary.py': (2653, 'b0230c062e19ba039746149fd212f965e397205ee599bdd145bed8f0775efe7f'),
 'source/tests/test_varchar_lifecycle.py': (2328, '4d79a9df05fa16fc4f6bceb663ec4314ba4ff8b7a3e5bf87e7471b3d2f45b35e'),
 'source/tests/test_varchar_runtime.py': (1874, '7357c5e27e8503b3f5aa4fc07af31e04ffa280e690bb336fbcb5eeb43c3fd53a'),
 'source/tests/test_warm_mapper_attachment.py': (1899, '7c680799d576f90f1dd91a7f8d94a9957401297d9b1b7f96a58ae67f8de7ae5f'),
 'source/tests/test_warm_worker_maintenance_fence.py': (7532, '7aa02c574306951bfec0932699d1fd27fdd31efe702754cf144b04ae0120a30f'),
 'source/uv.lock': (103898, 'faae077d223037c4a7d9a54e1aafc4760cf217057eb18fbd93fc021908be343e')}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def hex_digest(value, length=64):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(length) + '}', value) is not None


def safe_relative(name):
    require(isinstance(name, str) and bool(name), 'Path is not nonempty text')
    require(name.isascii() and '\\' not in name and all(32 <= ord(c) < 127 for c in name), 'Unsafe path character')
    require(all(c not in ('', '.', '..') for c in name.split('/')), 'Noncanonical path component')
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name, 'Noncanonical relative path')
    return path


def allowed_name(name):
    path = safe_relative(name)
    folded = {p.casefold() for p in path.parts}
    require(path.name.casefold() not in FORBIDDEN_LEAVES and not folded & FORBIDDEN_PARTS, 'Forbidden raw phase/runtime/dependency/credential path')
    require(not any(p == '.env' or p.startswith('.env.') for p in folded), 'Forbidden environment path')
    require(not path.name.casefold().endswith(('.pyc', '.pyo', '.sqlite', '.sqlite3', '.db', '.tar', '.tar.xz', '.tar.gz', '.tgz', '.zip', '.bin', '.pem', '.key')), 'Forbidden runtime/nested archive/credential file')
    return path


def validate_names(names):
    require(names == sorted(set(names)), 'Names are not sorted unique exact closure')
    require(len(names) == len({n.casefold() for n in names}), 'Case-colliding filenames')
    files = set(names)
    directories = set()
    for name in names:
        path = allowed_name(name)
        for parent in path.parents:
            if parent.as_posix() != '.':
                require(parent.as_posix() not in files, 'File/directory collision')
                directories.add(parent.as_posix())
    all_names = files | directories
    require(len(all_names) == len({n.casefold() for n in all_names}), 'Case-colliding file/directory paths')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON object key')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('Nonfinite JSON value')


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode('utf-8')


def require_directory(path):
    require(stat.S_ISDIR(path.lstat().st_mode), 'Non-directory or symlink ancestor')


def require_directory_chain(path):
    require(path.is_absolute(), 'Directory is not absolute')
    for ancestor in reversed(path.parents):
        require_directory(ancestor)
    require_directory(path)


def open_directory(path):
    """Open every directory relative to an already-open, no-follow ancestor."""
    require(path.is_absolute(), 'Directory is not absolute')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in path.parts[1:]:
            new_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = new_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_regular(path, limit):
    require(path.is_relative_to(P), 'Read outside fixed recovery namespace')
    require(type(limit) is int and limit >= 0, 'Invalid read bound')
    parent_fd = open_directory(path.parent)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        require(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= limit, 'Input is not a bounded regular file')
        data = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'Input changed while reading')
    require(len(data) == before.st_size and len(data) <= limit, 'Input length changed or bound exceeded')
    return data


def absent(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return True
    return False


def new_directory(path):
    require(path.is_relative_to(P), 'Directory outside fixed recovery namespace')
    parent_fd = open_directory(path.parent)
    try:
        os.mkdir(path.name, mode=0o700, dir_fd=parent_fd)
    finally:
        os.close(parent_fd)
    require_directory_chain(path)


def write_new(root, relative, data):
    require(root.is_relative_to(P), 'Write outside fixed recovery namespace')
    components = safe_relative(relative).parts
    parent_fd = open_directory(root)
    try:
        for component in components[:-1]:
            try:
                os.mkdir(component, mode=0o700, dir_fd=parent_fd)
            except FileExistsError:
                pass
            child_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
            os.close(parent_fd)
            parent_fd = child_fd
        fd = os.open(components[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent_fd)
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), 0o600)
            require(stream.write(data) == len(data), 'Short write')
    finally:
        os.close(parent_fd)
    require(read_regular(root / relative, len(data)) == data, 'New output readback differs')


def verify_tree(root, expected):
    require_directory_chain(root)
    files, directories = set(), set()
    want_dirs = {p.as_posix() for name in expected for p in safe_relative(name).parents if p.as_posix() != '.'}
    for current, subdirs, leaves in os.walk(root, followlinks=False):
        for name in subdirs + leaves:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            safe_relative(relative)
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                directories.add(relative)
            else:
                require(stat.S_ISREG(mode) and stat.S_IMODE(mode) == 0o600, 'Restored link/special/non-inert mode')
                require(relative in expected and read_regular(path, len(expected[relative])) == expected[relative], 'Restored name/bytes differ')
                files.add(relative)
    require(files == set(expected) and directories == want_dirs, 'Fresh tree file/directory closure differs')


def ustar_header(name, size):
    """Canonical ordinary USTAR header; exact equality rejects all extensions."""
    encoded = name.encode('ascii')
    prefix, leaf = b'', encoded
    if len(encoded) > 100:
        parts = encoded.split(b'/')
        for index in range(1, len(parts)):
            left, right = b'/'.join(parts[:index]), b'/'.join(parts[index:])
            if len(left) <= 155 and len(right) <= 100:
                prefix, leaf = left, right
                break
        else:
            raise ValueError('USTAR path does not fit')
    header = bytearray(512)
    def put(offset, width, value):
        require(len(value) <= width, 'USTAR header field overflow')
        header[offset:offset + width] = value.ljust(width, b'\0')
    def octal(number, width):
        return format(number, '0' + str(width - 1) + 'o').encode('ascii') + b'\0'
    put(0, 100, leaf)
    put(100, 8, octal(0o644, 8))
    put(108, 8, octal(0, 8))
    put(116, 8, octal(0, 8))
    put(124, 12, octal(size, 12))
    put(136, 12, octal(0, 12))
    header[148:156] = b'        '
    header[156:157] = b'0'
    header[257:265] = b'ustar\00000'
    put(345, 155, prefix)
    header[148:156] = format(sum(header), '06o').encode('ascii') + b'\0 '
    return bytes(header)


def evidence_reference(value):
    return isinstance(value, str) and 0 < len(value) <= 4096 and value.strip() == value and all(ord(c) >= 32 and ord(c) != 127 for c in value)


def authenticate_inputs(commit, receipt_hash):
    require_directory_chain(PARTS)
    wanted_names = {row[0] for row in EXPECTED_REMOTE_FILES} | {'REMOTE_PROVENANCE.json'}
    require({p.name for p in PARTS.iterdir()} == wanted_names, 'Remote readback directory exact closure differs')
    receipt_bytes = read_regular(PARTS / 'REMOTE_PROVENANCE.json', 100000)
    require(sha256(receipt_bytes) == receipt_hash, 'Provenance is not independently pinned identity')
    receipt = parse_json(receipt_bytes)
    keys = {'format', 'authenticated_remote_readbacks_verified', 'repository', 'remote_prefix', 'commit_sha', 'authenticated_commit_lookup', 'commit_lookup_sha', 'commit_lookup_reference', 'archive_sha256', 'part_manifest_sha256', 'independent_archive_review_sha256', 'local_readback_directory', 'source', 'local_staging_used_for_restore', 'remote_files'}
    require(isinstance(receipt, dict) and set(receipt) == keys, 'Provenance schema differs')
    require(receipt['format'] == 'async-cleanup-authenticated-remote-provenance-v1', 'Provenance format differs')
    require(receipt['authenticated_remote_readbacks_verified'] is True and receipt['authenticated_commit_lookup'] is True, 'Actual authenticated readback or commit attestation absent')
    require(receipt['repository'] == REPOSITORY and receipt['remote_prefix'] == REMOTE_PREFIX, 'Provenance repository/prefix differs')
    require(receipt['commit_sha'] == commit and receipt['commit_lookup_sha'] == commit, 'Independently pinned immutable commit differs')
    require(evidence_reference(receipt['commit_lookup_reference']), 'Authenticated commit evidence reference absent')
    require(receipt['archive_sha256'] == ARCHIVE_SHA256 and receipt['part_manifest_sha256'] == PART_MANIFEST_SHA256, 'Provenance capsule pins differ')
    require(receipt['independent_archive_review_sha256'] == INDEPENDENT_REVIEW_SHA256, 'Independent archive acceptance pin differs')
    require(receipt['local_readback_directory'] == str(PARTS), 'Readback input directory differs')
    require(receipt['source'] == 'authenticated_remote_readback' and receipt['local_staging_used_for_restore'] is False, 'Local staging cannot substitute for remote readbacks')
    rows = receipt['remote_files']
    require(isinstance(rows, list) and len(rows) == 12, 'Twelve individual remote readbacks required')
    inputs = {}
    for row, (name, size, digest, blob) in zip(rows, EXPECTED_REMOTE_FILES):
        require(isinstance(row, dict) and set(row) == {'name', 'repository', 'commit_sha', 'remote_path', 'authenticated_readback', 'bytes', 'sha256', 'git_blob_sha', 'verification_reference'}, 'Per-file receipt schema differs')
        require(row['name'] == name and row['repository'] == REPOSITORY and row['commit_sha'] == commit, 'Per-file same-commit/repository/name differs')
        require(row['remote_path'] == REMOTE_PREFIX + '/' + name and row['authenticated_readback'] is True, 'Per-file remote path/authentication differs')
        require(type(row['bytes']) is int and row['bytes'] == size and row['sha256'] == digest and row['git_blob_sha'] == blob, 'Per-file identity differs')
        require(evidence_reference(row['verification_reference']), 'Per-file authenticated evidence reference absent')
        data = read_regular(PARTS / name, size)
        require(len(data) == size and sha256(data) == digest and git_blob(data) == blob, 'Remote readback body differs: ' + name)
        inputs[name] = data
    return receipt_bytes, inputs, wanted_names


def admit_archive(archive_bytes):
    require(len(archive_bytes) == ARCHIVE_BYTES and sha256(archive_bytes) == ARCHIVE_SHA256, 'Recombined archive identity differs')
    names = sorted(EXPECTED_MEMBERS)
    validate_names(names)
    require(len(names) == MEMBERS and sum(v[0] for v in EXPECTED_MEMBERS.values()) == TOTAL_MEMBER_BYTES, 'Embedded exact member closure differs')
    for size, digest in EXPECTED_MEMBERS.values():
        require(type(size) is int and 0 <= size <= MAX_MEMBER_BYTES and hex_digest(digest), 'Invalid embedded size/hash')
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=64 * 1024 * 1024)
    raw = decoder.decompress(archive_bytes, max_length=TAR_BYTES + 1)
    require(len(raw) == TAR_BYTES and decoder.eof and not decoder.unused_data and decoder.check == lzma.CHECK_CRC64, 'XZ size/check/stream bound differs')
    positions, offset = {}, 0
    # Validate the COMPLETE member name/type/size/order/header closure before
    # slicing, hashing, parsing or otherwise reading ANY archive member body.
    for name in names:
        size, digest = EXPECTED_MEMBERS[name]
        require(raw[offset:offset + 512] == ustar_header(ARCHIVE_ROOT + '/' + name, size), 'Noncanonical USTAR member name/type/header/order/size: ' + name)
        begin = offset + 512
        end = begin + size
        padded_end = (end + 511) // 512 * 512
        require(padded_end <= len(raw) and raw[end:padded_end] == bytes(padded_end - end), 'Member bound or zero padding differs')
        positions[name] = (begin, end)
        offset = padded_end
    require(len(raw) - offset >= 1024 and raw[offset:] == bytes(len(raw) - offset), 'Tar tail differs')
    require(len(raw) == ((offset + 1024 + 10239) // 10240) * 10240, 'Canonical terminal record padding differs')
    payload = {}
    for name in names:
        begin, end = positions[name]
        body = raw[begin:end]
        size, digest = EXPECTED_MEMBERS[name]
        require(len(body) == size and sha256(body) == digest, 'Admitted member bytes differ: ' + name)
        payload[name] = body
    return payload


def verify_payload(payload):
    manifest = parse_json(payload[MANIFEST_NAME])
    require(len(payload[MANIFEST_NAME]) == MANIFEST_BYTES and sha256(payload[MANIFEST_NAME]) == MANIFEST_SHA256, 'Frozen manifest differs')
    expected_map = {n: {'size': size, 'sha256': digest} for n, (size, digest) in EXPECTED_MEMBERS.items() if n != MANIFEST_NAME}
    require(manifest['files'] == expected_map and len(manifest['files']) == MEMBERS - 1, 'Exact frozen manifest member map differs')
    require(manifest['schema'] == 1 and type(manifest['schema']) is int and manifest['archive_root'] == ARCHIVE_ROOT and manifest['self_excluded'] == MANIFEST_NAME, 'Frozen manifest schema/root differs')
    require(manifest['archive_member_count'] == MEMBERS and manifest['payload_bytes_excluding_manifest'] == TOTAL_MEMBER_BYTES - MANIFEST_BYTES, 'Frozen manifest totals differ')
    require(manifest['original_input_count'] == 482 and manifest['original_input_bytes'] == 8166671 and manifest['prepared_document_count'] == 2 and manifest['source_file_count'] == SOURCE_COUNT, 'Frozen selected-data scope differs')
    require(manifest['status'] == 'AUTHORIZED_LOCAL_DATA_ONLY_FREEZE_PENDING_INDEPENDENT_ARCHIVE_REVIEW', 'Frozen historical status differs')
    require(manifest['allowlist_sha256'] == '442857ea6560e7600566eee05823f968d58e9c2df0feccb98f05af82e3dce173' and manifest['prepared_inputs_sha256'] == 'aadaf38be9c80103fbdf90f736491fbe928a1acb918180c1d2100a0f3aacafc7', 'Prepared input pins differ')
    require(sha256(payload[ALLOWLIST_NAME]) == ALLOWLIST_SHA256, 'Frozen exact allowlist differs')
    allow = parse_json(payload[ALLOWLIST_NAME])
    require(allow['exact_archive_member_names'] == sorted(EXPECTED_MEMBERS), 'Exact admitted member allowlist differs')
    require(set(allow['external_outputs_excluded']) == {ARCHIVE_NAME, ARCHIVE_NAME + '.sha256', 'REBUILD_CHECK-v1.json', 'RESTORE_VERIFICATION-v1.json'}, 'Excluded outputs differ')
    selected = parse_json(payload['freeze/preparation/COPY_ALLOWLIST.json'])['files']
    prepared = parse_json(payload['freeze/preparation/PREPARED_INPUTS.json'])['files']
    validated = parse_json(payload['freeze/independent-review/VALIDATED_INPUTS.json'])
    require(len(selected) == 482 and selected == validated and len(prepared) == 482, 'Selected prepared/accepted input closure differs')
    prepared_map = {row['destination']: row for row in prepared}
    require(len(prepared_map) == 482 and set(prepared_map) == {row['destination'] for row in selected}, 'Selected destination map differs')
    total = 0
    for row in selected:
        name = row['destination']
        allowed_name(name)
        pin = prepared_map[name]
        require(name in payload and pin['source'] == row['source'] and pin['category'] == row['category'], 'Selected input mapping differs')
        require(type(pin['bytes']) is int and pin['bytes'] == len(payload[name]) and pin['sha256'] == sha256(payload[name]), 'Selected input bytes differ')
        total += len(payload[name])
    require(total == 8166671, 'Selected input byte total differs')
    # Source paths mentioned by these documents remain inert strings. Never
    # follow them to live files, dependencies, environments or original runs.
    packet = 'experiments/next-unblocked-correctness-20261014/'
    source = {name[len('source/'):]: body for name, body in payload.items() if name.startswith('source/')}
    validate_names(sorted(source))
    green = parse_json(payload[packet + 'GREEN_SOURCE_MANIFEST.json'])['source_sha256']
    red = parse_json(payload[packet + 'RED_SOURCE_MANIFEST.json'])['source_sha256']
    baseline = parse_json(payload[packet + 'BASELINE_SOURCE_MANIFEST.json'])['source_sha256']
    source_allow = payload['freeze/preparation/SOURCE_FILENAME_ALLOWLIST.txt'].decode('ascii').splitlines()
    require(source_allow == sorted(set(source_allow)) and set(source_allow) == set(source) == set(green) and len(source) == SOURCE_COUNT, 'Full217 source exact closure differs')
    require(sum(map(len, source.values())) == SOURCE_BYTES, 'Full217 source byte total differs')
    source_hashes = {name: sha256(body) for name, body in source.items()}
    require(source_hashes == green, 'Full217 GREEN source hashes differ')
    restored_red = dict(source_hashes)
    restored_red['src/cryptalis/sqlalchemy.py'] = sha256(payload[packet + 'BASELINE_sqlalchemy.py'])
    require(restored_red == red and len(red) == SOURCE_COUNT, 'RED byte reconstruction differs')
    restored_baseline = dict(restored_red)
    del restored_baseline['tests/test_sqlalchemy_async_exit_double_failure.py']
    require(restored_baseline == baseline and len(baseline) == 216, 'Baseline byte reconstruction differs')
    require([name for name in sorted(red) if red[name] != green[name]] == ['src/cryptalis/sqlalchemy.py'], 'Sole RED/GREEN source delta differs')
    return source


def main():
    parser = argparse.ArgumentParser(description='Inert offline restore requiring independently pinned actual remote provenance')
    parser.add_argument('--expected-remote-commit', required=True)
    parser.add_argument('--authenticated-provenance-sha256', required=True)
    args = parser.parse_args()
    require(hex_digest(args.expected_remote_commit, 40), 'Expected immutable commit must be forty lowercase hex characters')
    require(hex_digest(args.authenticated_provenance_sha256), 'Expected provenance SHA-256 must be sixty-four lowercase hex characters')
    require_directory_chain(P)
    outputs = (OUTARCHIVE, OUTROOT, OUTSOURCE, OUTREPORT)
    for output in outputs:
        require(absent(output), 'Fresh output already exists; never reuse or overwrite: ' + output.name)
    receipt_bytes, inputs, wanted_names = authenticate_inputs(args.expected_remote_commit, args.authenticated_provenance_sha256)
    split = parse_json(inputs['MANIFEST.json'])
    require(split == EXPECTED_PART_MANIFEST, 'Exact split manifest differs')
    archive = b''.join(inputs[row[0]] for row in EXPECTED_PARTS)
    payload = admit_archive(archive)
    source = verify_payload(payload)
    # Every input, complete archive closure and every body is now verified.
    # No archive script is imported, compiled, launched or executed.
    for output in outputs:
        require(absent(output), 'Output appeared before writing: ' + output.name)
    write_new(P, OUTARCHIVE.name, archive)
    new_directory(OUTROOT)
    for name, body in payload.items():
        write_new(OUTROOT, name, body)
    new_directory(OUTSOURCE)
    for name, body in source.items():
        write_new(OUTSOURCE, name, body)
    verify_tree(OUTROOT, payload)
    verify_tree(OUTSOURCE, source)
    require(read_regular(OUTARCHIVE, ARCHIVE_BYTES) == archive, 'Reconstructed archive readback differs')
    require(read_regular(PARTS / 'REMOTE_PROVENANCE.json', 100000) == receipt_bytes, 'Provenance changed during restore')
    for name, body in inputs.items():
        require(read_regular(PARTS / name, len(body)) == body, 'Remote readback changed during restore')
    require({p.name for p in PARTS.iterdir()} == wanted_names, 'Remote input directory changed')
    report = {
        'status': 'PASS_COORDINATOR_AUTHENTICATED_REMOTE_DATA_ONLY_CLEANUP_RESTORE',
        'repository': REPOSITORY, 'remote_commit_sha': args.expected_remote_commit, 'remote_prefix': REMOTE_PREFIX,
        'authenticated_provenance_sha256': sha256(receipt_bytes),
        'authentication_scope': 'Exact externally authenticated and independently pinned commit plus twelve per-file readback receipts; this offline checker cannot authenticate a network service or distinguish dishonestly relabeled staging bytes.',
        'archive_sha256': ARCHIVE_SHA256, 'archive_bytes': ARCHIVE_BYTES, 'tar_bytes': TAR_BYTES,
        'part_manifest_sha256': PART_MANIFEST_SHA256, 'parts_verified': 11, 'remote_files_verified': 12,
        'frozen_manifest_sha256': MANIFEST_SHA256, 'exact_allowlist_sha256': ALLOWLIST_SHA256,
        'independent_archive_review_sha256': INDEPENDENT_REVIEW_SHA256,
        'exact_regular_members': MEMBERS, 'member_bytes': TOTAL_MEMBER_BYTES,
        'complete_name_type_header_bounds_before_member_body_reads': True,
        'restored_full217source_files': len(source), 'restored_full217source_bytes': SOURCE_BYTES,
        'green_source_hashes_verified': True, 'red_and_baseline_byte_reconstruction_verified': True,
        'extraction_directory': str(OUTROOT), 'full217source_directory': str(OUTSOURCE),
        'all_restored_files_mode': '0600', 'complete_output_and_input_readbacks_verified': True,
        'focused_recorded_results': {'red_sa20': {'nodes': 22, 'failed': 13, 'passed': 9}, 'red_sa21': {'nodes': 22, 'failed': 13, 'passed': 9}, 'green_sa20': {'nodes': 46, 'passed': 46}, 'green_sa21': {'nodes': 46, 'passed': 46}},
        'recorded_results_scope': 'Preserved accepted byte evidence only; no fresh runtime result or separate node reconciliation is claimed.',
        'all_seven_gates': 'UNKNOWN', 'historical_seven_acceptance_failures': 'Unresolved prior disposition preserved; not rerun or reclassified.',
        'full_suite_current_run_included': False, 'full_matrix_qualification': 'PENDING_SEPARATE', 'installed_qualification': 'PENDING_SEPARATE',
        'synthetic_fixture_disposition_sha256': '640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022',
        'synthetic_fixture_dispositions_preserved': 2, 'new_secret_scan_performed': False,
        'security_qualification_or_universal_quarantine_claimed': False, 'operational_environment_restore_claimed': False,
        'runtime_dependency_database_state_restored': False, 'archive_code_executed': False,
        'product_imports_tests_network_git_databases_subprocesses': False,
    }
    write_new(P, OUTREPORT.name, json_bytes(report))
    print(json.dumps({'status': report['status'], 'report': str(OUTREPORT), 'archive_sha256': ARCHIVE_SHA256, 'full217source_files': len(source)}, sort_keys=True))


if __name__ == '__main__':
    main()
