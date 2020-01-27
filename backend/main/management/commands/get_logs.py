from django.core.management.base import BaseCommand, CommandError
from main.models import Log
from django.utils import timezone
import sys
import os
import re
import datetime
from tqdm import tqdm
import urllib.request 


class Command(BaseCommand):
        
    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start loading data'))
        self.url = options['url'][0]
        self.size_limit = 100 * 1024 * 1024
        filename = self.url.split('/')[-1]
        self.filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        self.data = []
        
        try:
            self.download()
        except Exception as err:
            self.stdout.write(self.style.ERROR(f'Error while donloading file: {err}'))
            return

        try:
            self.parse()
        except Exception as err:
            self.stdout.write(self.style.ERROR(f'Error while parsing data: {err}'))
            return
        
        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))

    def download(self):
        req = urllib.request.Request(url=self.url, method='HEAD')
        content_length = int(dict(urllib.request.urlopen(req).info())['Content-Length'])
        if content_length > self.size_limit:
            self.stdout.write(self.style.ERROR('!!! ATENTION !!!'))
            self.stdout.write(self.style.ERROR(
                f'Remote file too large, downloading will be limited to {self.size_limit / 1024 / 1024 }Mb'))
            content_length = self.size_limit

        current_size = 0

        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, desc='Downloading', total=content_length) as p:
            with open(self.filepath, 'wb') as file:
                for chunk in urllib.request.urlopen(self.url):
                    file.write(chunk)
                    p.update(len(chunk))
                    current_size += len(chunk)
                    if current_size >= self.size_limit:
                        break

    def parse(self):
        part = []
        cnt = 0
        pattern = re.compile(r'(?P<ip_address>.*?) - - \[(?P<timestamp>.*?) \+\d+\] "(?P<http_method>.*?) (?P<uri>.*?) HTTP/1.*?" (?P<status_code>\d+) (?P<content_length>\d+) "(?P<referer>.*?)" "(?P<user_agent>.*?)".*')

        with open(self.filepath, 'r') as file:
            filesize = os.fstat(file.fileno()).st_size
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, total=filesize, desc='Parsing') as p:
                for line in file:
                    match_item = pattern.match(line)
                    if match_item:
                        item = match_item.groupdict()
                        try:
                            item['http_method'] = Log.http_methods[item['http_method'].upper()]
                        except:
                            p.update(len(line) + 1)
                            continue

                        item['timestamp'] = datetime.datetime.strptime(item['timestamp'], '%d/%b/%Y:%H:%M:%S').replace(tzinfo=timezone.utc)

                        part.append(Log(**item))
                        cnt += 1
                        if cnt == 1000:
                            Log.objects.bulk_create(part) 
                            part = []
                            cnt = 0

                    p.update(len(line) + 1)
                    
                if cnt:
                    Log.objects.bulk_create(part) 
