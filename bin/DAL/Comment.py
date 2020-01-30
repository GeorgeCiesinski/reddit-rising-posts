#!/user/bin/python3


class Comment:
	@staticmethod
	def comment_detail_upsert(pg, comment):
		with pg.cursor() as cur:
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
			cur.execute(
				"select comment_snapshot_insert(%s, %s)",
				(
					comment.id,
					comment.score,
				)
			)
		return True
