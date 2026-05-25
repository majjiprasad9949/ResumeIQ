export default function ScoreDisplay({ score, riskLevel }) {
  const getRiskColor = (level) => {
    switch (level) {
      case 'low':
        return 'text-green-600 bg-green-50';
      case 'moderate':
        return 'text-yellow-600 bg-yellow-50';
      case 'high':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getRiskBadgeColor = (level) => {
    switch (level) {
      case 'low':
        return 'bg-green-100 text-green-800';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800';
      case 'high':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className={`rounded-lg shadow p-8 text-center ${getRiskColor(riskLevel)}`}>
      <div className="text-6xl font-bold text-blue-600 mb-4">{score.toFixed(1)}</div>
      <div className="text-xl text-gray-600 mb-4">ATS Score</div>
      <div className={`inline-block px-4 py-2 rounded-full font-semibold ${getRiskBadgeColor(riskLevel)}`}>
        {riskLevel?.toUpperCase()} RISK
      </div>
    </div>
  );
}
