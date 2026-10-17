class TransitionFailure(RuntimeError):
    """Safe, actionable failure; durable progress requires current inspection."""
    effects = 'INSPECT_JOURNAL'
    retry = 'after_inspection'
    def __init__(self, code, operation_id=None, sqlstate=None, *, cleanup_errors=()):
        self.code, self.operation_id, self.sqlstate = code, operation_id, sqlstate
        self.cleanup_errors = tuple(cleanup_errors)
        cleanup = ''.join(f' cleanup={stage}:{cause}:{state or "UNKNOWN"};'
                          for stage,cause,state in self.cleanup_errors)
        remedy = {
            'legacy_profile_creation_disabled': ' New plans require the versioned native-designation inventory. Omit preserve_cluster_designation or set it to True. Existing artifact readers and safe recovery remain available.',
            'legacy_designation_evidence_required': ' Preserve ciphertext, application access, manifests, journal and backups. This historical artifact permits native index retirement without recording designation. Before any effects, replace it with a fresh inventoried plan using the still-existing native metadata. Before switch, use the existing safe abort path; a retained abort journal still requires reviewed replan handling. After retirement, supply independently authenticated pre-transition table/index/linkage/designation evidence bound to this target and artifact through a separately reviewed recovery procedure. Current flag absence or arbitrary JSON is insufficient; no evidence importer is implemented here.',
            'legacy_transient_designation_requires_review': ' The current designated index is a disposable transition companion. Keep protection and recovery material. Review an explicit metadata recovery plan before deprotection; do not silently clear the designation.',
            'other_database_snapshots_active': ' Finish or roll back other database transactions, then inspect and resume the same operation.',
            'unsupported_reverse_suffix_metadata': ' Ordered reverse copying currently requires ordinary text suffix columns without custom metadata or dependencies. Keep protection enabled; use a separately reviewed full-schema repair for other layouts.',
            'reverse_staging_layout_requires_inspection': ' Preserve this journal and staging data. Do not resume it with a different staging layout; inspect the recorded version and use a reviewed upgrade plan.',
        }.get(code, '')
        super().__init__(f'{code}; operation={operation_id or "unstarted"}; SQLSTATE={sqlstate or "UNKNOWN"}. '
                         'Keep writers stopped. Inspect this operation and the external current policy before resume.' + remedy + cleanup)
