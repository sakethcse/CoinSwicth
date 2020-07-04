from crontab import CronTab

my_cron = CronTab(user='saketh')

#my_cron.remove(comment='saketh_cron')
for job in my_cron:
	if job.comment == 'saketh_cron':
		my_cron.remove(job)
		my_cron.write()
		