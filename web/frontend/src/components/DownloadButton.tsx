import { getDownloadUrl } from "../api";

interface DownloadButtonProps {
  sessionId: string | null;
  disabled?: boolean;
}

export function DownloadButton({ sessionId, disabled }: DownloadButtonProps) {
  if (!sessionId) return null;
  const url = getDownloadUrl(sessionId);
  return (
    <a
      href={url}
      download="profile.md"
      className="download-btn"
      aria-disabled={disabled}
      style={{ pointerEvents: disabled ? "none" : undefined }}
    >
      下载画像
    </a>
  );
}
