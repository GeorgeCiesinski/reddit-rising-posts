#!/user/bin/python3


class Comment:
	@staticmethod
	def comment_detail_upsert(pg, comment):
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Insert the comment details
			cur.execute(
				"select comment_detail_upsert(%s, %s, %s)",
				(
					comment.id,
					comment.link_id,  # Submission ID
					comment.created_utc,
				)
			)

		return True

	@staticmethod
	def comment_snapshot_insert(pg, comment):
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Insert the comment snapshot
			cur.execute(
				"select comment_snapshot_insert(%s, %s)",
				(
					comment.id,
					comment.score,
				)
			)

			# Reschedule the comment
		return True

	@staticmethod
	def schedule_upsert(pg, comment_id, snapshot_frequency=300, next_snap=None) -> bool:
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Upsert the schedule row
			cur.execute(
				"select comment_control_upsert(%s, %s, %s)",
				(
					comment_id,
					snapshot_frequency,
					next_snap  # None = default
				)
			)
		return True

	@staticmethod
	def reschedule(pg, comment_id: str, snapshot_frequency: int = None, next_crawl: str = None) -> bool:
		with pg.cursor() as cur:
			# TODO: validate the input datatypes

			# Insert the comment snapshot
			cur.execute(
				"select reschedule_comment(%s, %s, %s)",
				(
					comment_id,
					snapshot_frequency,
					next_crawl
				)
			)

		# Reschedule the comment
		return True
