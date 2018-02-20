### FIRST INSTALL vaderSentiment package
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# to do:
# 1. determine how sql queries connect to this
# 2. generate scores for prof, department, and course (over all sections and 
# quarters) for comparison

data = pd.read_json('evals_json_version_4_part1.dms')
analyzer = SentimentIntensityAnalyzer()

course = data.loc[2] # EXAMPLE ONLY, actual course will come from sql query

course_responses_scores = {'compound': 0, 'neg': 0, 'neu': 0, 'pos': 0}
instructor_responses_scores = {'compound': 0, 'neg': 0, 'neu': 0, 'pos': 0}

# calculate total sentiment scores
for eval_ in course.course_responses:
    scores = analyzer.polarity_scores(eval_)
    course_responses_scores['compound'] += scores['compound'] # not sure if this measure is useful/necessary
    course_responses_scores['neg'] += scores['neg']
    course_responses_scores['neu'] += scores['neu']
    course_responses_scores['pos'] += scores['pos']

for eval_ in course.instructor_responses:
    scores = analyzer.polarity_scores(eval_)
    instructor_responses_scores['compound'] += scores['compound']
    instructor_responses_scores['neg'] += scores['neg']
    instructor_responses_scores['neu'] += scores['neu']
    instructor_responses_scores['pos'] += scores['pos']

# calculate average sentiment scores
for key, value in course_responses_scores.items():
    course_responses_scores[key] /= len(course.course_responses)

for key, value in instructor_responses_scores.items():
    instructor_responses_scores[key] /= len(course.instructor_responses)