export function Gauge({ score }: { score: number }) {
  const angle = -90 + (score / 100) * 180;
  return (
    <div className="gauge-wrap" role="img" aria-label={`Kreppumælir score ${score} of 100`}>
      <svg viewBox="0 0 220 130" width="100%" height="180" aria-hidden="true">
        <path d="M25 110a85 85 0 0 1 170 0" fill="none" stroke="#d8e6d6" strokeWidth="18" strokeLinecap="round" />
        <path
          d="M25 110a85 85 0 0 1 170 0"
          fill="none"
          stroke="#246f56"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray="88 267"
        />
        <path
          d="M25 110a85 85 0 0 1 170 0"
          fill="none"
          stroke="#b46f00"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray="88 267"
          strokeDashoffset="-88"
        />
        <path
          d="M25 110a85 85 0 0 1 170 0"
          fill="none"
          stroke="#b92d2a"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray="91 267"
          strokeDashoffset="-176"
        />
        <path
          d="M25 110a85 85 0 0 1 170 0"
          fill="none"
          stroke="#151914"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray={`${score * 2.67} 267`}
          opacity="0.18"
        />
        <line
          x1="110"
          y1="110"
          x2="110"
          y2="38"
          stroke="#171512"
          strokeWidth="5"
          strokeLinecap="round"
          transform={`rotate(${angle} 110 110)`}
        />
        <circle cx="110" cy="110" r="8" fill="#171512" />
      </svg>
      <div className="gauge-text">{score}</div>
      <p className="muted" style={{ textAlign: "center", margin: 0 }}>
        af 100 mögulegum kreppupunktum
      </p>
      <div className="gauge-label" aria-hidden="true">
        <span>rólegt</span>
        <span>Excel svitnar</span>
        <span>2008</span>
      </div>
    </div>
  );
}
