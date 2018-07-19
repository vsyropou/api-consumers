
from google.cloud import language, videointelligence
from google.cloud.language import enums
from google.cloud.language import types

from general import MessageService

error = MessageService.error
info  = MessageService.info
warn  = MessageService.warn
debug = MessageService.debug

import six
import os
import abc

class AbsGoogleApi(abc.ABC):
    
    @abc.abstractmethod
    def consume(self,obj):
        pass
    
class BaseGoogleApi(AbsGoogleApi):

    def __init__(self):

        self._check_credentials()

    def _check_credentials(self):
        # TODO: Handle some exceptions here
        CRED_VAR_NAME = 'GOOGLE_APPLICATION_CREDENTIALS' 
        
        if not CRED_VAR_NAME in os.environ.keys():
            msg = 'Provide full path to credentials file in order to authenticate with Google Api services:\n> '
            credentials_path = input(msg)
            print()

            os.environ[CRED_VAR_NAME] = credentials_path

        assert os.path.exists(os.environ[CRED_VAR_NAME])


class ClasifyTextGoogleApi(BaseGoogleApi):

    def consume(self,text,**kwargs):
        """Classifies content categories of the provided text."""

        ## TODO: add concurency in case of list of objects
        client = language.LanguageServiceClient()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        categories = client.classify_text(document).categories

        ##TODO: Use formaters here as in MSsqlDatabaseTool
        return [ {'label':x.name, 'confidence':x.confidence} for x in categories]


class AnalyzeSyntaxGoogleApi(BaseGoogleApi):
    """Detects syntax in the text."""

    def consume(self,text,**kwargs):
    
        client = language.LanguageServiceClient()

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Instantiates a plain text document.
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects syntax in the document. You can also analyze HTML with:
        #   document.type == enums.Document.Type.HTML
        tokens = client.analyze_syntax(document).tokens

        # part-of-speech tags from enums.PartOfSpeech.Tag
        pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
                   'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

        for token in tokens:
            print(u'  {}: {}'.format(pos_tag[token.part_of_speech.tag],
                                     token.text.content))


class AnnotaetVideoGoogleApi(BaseGoogleApi):
    ## TODO:: Make class for shots as well.
    
    def consume(self,path,**kwargs):
        """ Detects labels given a GCS path. """


        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.LABEL_DETECTION]

        mode = videointelligence.enums.LabelDetectionMode.SHOT_AND_FRAME_MODE
        config = videointelligence.types.LabelDetectionConfig(
            label_detection_mode=mode)
        context = videointelligence.types.VideoContext(
            label_detection_config=config)

        operation = video_client.annotate_video(path, features=features, video_context=context)

        info('Processing "%s" for label annotations:'%path)

        result = operation.result(timeout=10*60)
        info('Finished processing.')
        
        out = []
    
        # Process video/segment level label annotations
        segment_labels = result.annotation_results[0].segment_label_annotations
        for i, segment_label in enumerate(segment_labels):
            # print('Video label description: {}'.format(
              #   segment_label.entity.description))
            for category_entity in segment_label.category_entities:
                # print('\tLabel category description: {}'.format(
                #    category_entity.description))
                pass
            for i, segment in enumerate(segment_label.segments):
                start_time = (segment.segment.start_time_offset.seconds +
                              segment.segment.start_time_offset.nanos / 1e9)
                end_time = (segment.segment.end_time_offset.seconds +
                            segment.segment.end_time_offset.nanos / 1e9)
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = segment.confidence
                # print('\tSegment {}: {}'.format(i, positions))
                # print('\tConfidence: {}'.format(confidence))
            # print('\n')
    
            out.append( {'label':segment_label.entity.description,
                         'category':category_entity.description if segment_label.category_entities else '',
                         'start':start_time if segment_label.segments else '',
                         'end':end_time if segment_label.segments else '',
                         'confidence':confidence if segment_label.segments else ''
                         })
    
        return out
