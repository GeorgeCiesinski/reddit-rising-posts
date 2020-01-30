#!/user/bin/python3


class Submission:
	@staticmethod
	def submission_detail_upsert(pg, submission):
		cur = pg.cursor()
		cur.execute(
			"select submission_detail_upsert(%s, %s, %s, %s, %s, %s)",
			(
				submission.id,
				submission.subreddit,
				999,  # submission.author,
				submission.title,
				submission.created_utc,
				submission.url
			)
		)
		cur.close()
		return True

	@staticmethod
	def submission_snapshot_insert(pg, submission):
		cur = pg.cursor()
		cur.execute(
			"select submission_snapshot_insert(%s, %s, %s, %s)",
			(
				submission.id,
				submission.score,
				submission.num_comments,
				submission.upvote_ratio,
			)
		)
		cur.close()
		return True

	@staticmethod
	def submission_schedule_set(pg, submission, snapshot_frequency=300, next_snap=None):
		with pg.cursor() as cur:
			cur.execute(
				"select submission_control_set(%s, %s, %s)",
				(
					submission.id,
					snapshot_frequency,
					next_snap  # None = default
				)
			)

		return True
