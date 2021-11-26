# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 13:08:37 2021

@author: 91832
"""
#command to run this program :
#python -m RemoveChar --region asia --input gs://training-demo-project/devopsjob.csv  --o
#utput gs://training-demo-project/output/ --runner DataflowRunner --project de-training-project --temp_location gs://training-demo-project/temp --templat
#e_location gs://training-demo-project/templates/my_TEMPLATE




import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
import os
#set GOOGLE_APPLICATION_CREDENTIALS environment variable in Python code to the path key.json file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\91832\\Downloads\\de-training-project-d479812df9a5.json'


# defining custom arguments
class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--input', default='gs://training-demo-project/devopsjob.csv')
        parser.add_value_provider_argument('--output', default='gs://training-demo-project/devopsjobcleanfile.txt')


class Filterchar(beam.DoFn):
    def process(self, element):
        special_char = '@_!#$*()<>?/|\}{~:.;[]()"'
        for i in element:
            element = ''.join((filter(lambda i: i not in special_char, element)))
            return [element]

#class Split(beam.DoFn):
   # def process(self, element):
       # roles, companies, locations, experience, skills = element.split(",")
        #return [{
            #'roles': str(roles),
            #'companies': str(companies),
            #'locations': str(locations),
            #'experience':str(experience),
            #'skills': str(skills)
       # }]

# instantiate the pipeline
pipeline_options = PipelineOptions()
known_args = pipeline_options.view_as(UserOptions)
pipeline_options.view_as(SetupOptions).save_main_session = True

with beam.Pipeline() as pipeline:
    devopsjob = (
            pipeline | beam.io.ReadFromText(known_args.input, skip_header_lines=True)
            | beam.ParDo(Filterchar())
            #| beam.Map(print)
            #| beam.ParDo(Split())
            | "write to gcs" >> beam.io.WriteToText(known_args.output)
    )

pipeline.run()

