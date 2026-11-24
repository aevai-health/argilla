import { lowScoreCommentNeeded } from "./lowScoreComment";

const rating = (v) => ({ name: "accuracy", isRatingType: true, answer: { valuesAnswered: v } });
const comment = { name: "accuracy_comment" };

test.each([
  [undefined, false],
  [2, true],
  [3, false],
])("accuracy=%s -> comment needed %s", (v, expected) => {
  expect(lowScoreCommentNeeded(comment, [rating(v), comment])).toBe(expected);
});

test("other questions are always shown", () => {
  expect(lowScoreCommentNeeded({ name: "clarity" }, [])).toBe(true);
});
