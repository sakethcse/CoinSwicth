from crontab import CronTab

my_cron = CronTab(user='saketh')

my_job = my_cron.new(command='python3 /home/saketh/Desktop/TVLK/CompanyCodingTests/CoinSwitch/get_data.py' , comment = 'saketh_cron')
my_job.minute.every(1)
my_cron.write()