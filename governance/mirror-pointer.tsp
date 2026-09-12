namespace SonusAuris.Governance;

/** Synchronization state of a non-authoritative repository mirror. */
enum MirrorStatus {
  current,
  stale,
  blocked,
  unverified,
}

/** Pointer stored outside the canonical owner-level `.github` repository. */
model OrganizationSourceOfTruthPointer {
  schemaVersion: string;
  organization: string;
  authorityRepository: string;
  canonicalPath: string;
  canonicalRevision: int32;
  observedAt: string;
  status: MirrorStatus;
  /** Optional normalized canonical digest once a validator has computed it. */
  canonicalDigest?: string;
  /** Repository containing this pointer. */
  mirrorRepository: string;
  /** Must remain `pointer`; full mirrors use the canonical manifest model. */
  mirrorMode: string;
  note?: string;
}
