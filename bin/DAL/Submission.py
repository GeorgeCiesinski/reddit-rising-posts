#!/user/bin/python3


class Submission:
	@staticmethod
	def submission_detail_upsert(pg, submission):
		with pg.cursor() as cur:
			# Insert the submission details
			cur.execute(
				"select submission_detail_upsert(%s, %s, %s, %s, %s, %s)",
				(
					submission.id,
					submission.subreddit,
					'999',  # submission.author,
					submission.title,
					submission.created_utc,
					submission.url
				)
			)

		# Schedule the submission to get its snapshot scraped
		Submission.schedule_upsert(pg, submission.id)
		return True

	@staticmethod
	def submission_snapshot_insert(pg, submission):
		with pg.cursor() as cur:
			# Insert the snapshot of the submission
			cur.execute(
				"select submission_snapshot_insert(%s, %s, %s, %s)",
				(
					submission.id,
					submission.score,
					submission.num_comments,
					submission.upvote_ratio,
				)
			)

		# Reschedule the submission to get scraped again
		Submission.reschedule(pg, submission.id)
		return True

	@staticmethod
	def schedule_upsert(pg, submission_id: str, snapshot_frequency: int = 300, next_snap=None) -> bool:
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Upsert the control row
			cur.execute(
				"select submission_control_upsert(%s, %s, %s)",
				(
					submission_id,
					snapshot_frequency,
					next_snap  # None = default
				)
			)
		return True

	@staticmethod
	def reschedule(pg, submission_id: str, snapshot_frequency: int = None, next_crawl: str = None) -> bool:
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Insert the comment snapshot
			cur.execute(
				"select reschedule_comment(%s, %s, %s)",
				(
					submission_id,
					snapshot_frequency,
					next_crawl
				)
			)

		# Reschedule the comment
		return True
