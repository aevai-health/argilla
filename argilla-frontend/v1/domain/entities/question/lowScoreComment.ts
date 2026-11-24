// aevai: a question named "<rating>_comment" only shows, and is then required, while rating "<rating>" is below 3
export const lowScoreCommentNeeded = (question, questions): boolean => {
  if (!question.name.endsWith("_comment")) return true;
  const rating = questions.find(
    (q) => q.isRatingType && q.name === question.name.slice(0, -"_comment".length)
  );
  return !rating || rating.answer.valuesAnswered < 3;
};
