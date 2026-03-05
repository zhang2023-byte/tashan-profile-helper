import ReactMarkdown from "react-markdown";
import { getDownloadUrl, getForumDownloadUrl } from "../api";

interface ProfilePanelProps {
  sessionId: string | null;
  profile: string;
  forumProfile: string;
}

export function ProfilePanel({
  sessionId,
  profile,
  forumProfile,
}: ProfilePanelProps) {
  if (!sessionId) return null;

  return (
    <div className="profile-panel">
      <section className="profile-section">
        <h3>发展画像</h3>
        <div className="profile-content">
          {profile ? (
            <ReactMarkdown>{profile}</ReactMarkdown>
          ) : (
            <p className="profile-empty">尚未建立画像，可以说「帮我建立画像」开始。</p>
          )}
        </div>
        <a
          href={getDownloadUrl(sessionId)}
          download="profile.md"
          className="profile-download-btn"
        >
          下载发展画像
        </a>
      </section>

      <section className="profile-section">
        <h3>论坛画像</h3>
        <div className="profile-content">
          {forumProfile ? (
            <ReactMarkdown>{forumProfile}</ReactMarkdown>
          ) : (
            <p className="profile-empty">尚未生成论坛画像，可以说「生成论坛画像」或「数字分身」。</p>
          )}
        </div>
        <a
          href={getForumDownloadUrl(sessionId)}
          download="forum-profile.md"
          className="profile-download-btn"
          style={{ pointerEvents: forumProfile ? undefined : "none", opacity: forumProfile ? 1 : 0.5 }}
        >
          下载论坛画像
        </a>
      </section>
    </div>
  );
}
