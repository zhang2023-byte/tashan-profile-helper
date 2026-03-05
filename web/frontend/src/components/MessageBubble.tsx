import ReactMarkdown from "react-markdown";

interface MessageBubbleProps {
  role: "user" | "assistant";
  content: string;
}

export function MessageBubble({ role, content }: MessageBubbleProps) {
  const isUser = role === "user";
  return (
    <div
      className={`message-bubble ${isUser ? "user" : "assistant"}`}
      data-role={role}
    >
      {isUser ? (
        <p className="message-text">{content}</p>
      ) : (
        <div className="message-markdown">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
