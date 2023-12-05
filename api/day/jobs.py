import torch

from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from .models import Day


text_pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
)
image_pipe = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
)

text_pipe.to("mps")
image_pipe.to("mps")


@util.close_old_connections
def generate_day():
    dayObj = Day.objects.filter(day__isnull=False).order_by("-day").first()
    day = 1 if not dayObj or not dayObj.day else dayObj.day + 1
    Day.objects.create(day=day).generate_image(text_pipe, image_pipe)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class JobManager:
    def ready(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            generate_day,
            trigger=CronTrigger(minute="*/10"),
            id="generate_day",
            max_instances=1,
            replace_existing=True,
        )
            
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
