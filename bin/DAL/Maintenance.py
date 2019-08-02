#!/user/bin/python3

class Maintenance:
	@staticmethod
	def maint_correct_scrape_schedules(pg):
		cur = pg.cursor()
		# Correct all the scraping schedules
		cur.execute('select maint_correct_scrape_schedules()')
		cur.commit()
		cur.close()
		return True

	@staticmethod
	def maint_post_detail_sync(pg, post_id):
		cur = pg.cursor()
		# Correct all the scraping schedules
		cur.execute('select maint_post_detail_sync(%s)', (post_id,))
		cur.commit()
		cur.close()
		return True
