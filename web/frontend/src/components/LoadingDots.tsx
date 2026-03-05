/** 等待模型反馈时的可爱加载动画 */
export function LoadingDots() {
  return (
    <div className="loading-dots" aria-label="思考中">
      <span className="dot" />
      <span className="dot" />
      <span className="dot" />
    </div>
  );
}
