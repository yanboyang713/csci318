import openpyxl
import random
from commonTranslator import CommonTranslator
from fileManager import FileManager
from levDist import levenshteinDistance

"""
TestCaseManager
"""
class TestCaseManager:
	def __init__(self, results_file = 'testResults.xlsx'):
		self._translator = CommonTranslator()
		self._translation_file = FileManager()
		self._results_file = FileManager(results_file,
                                         [['Service', 'Test Phrase', 'Source Language', 'Intermediate Language', 'Target Language', 'Direct Translation', 'Alternate Translation'],
                                          ['Service', 'Source Language', 'Target Language', 'Lev-Distance']],
                                         ['Test Phrases', 'Test Results'],
                                         write_header = True)


	"""
	Verifies a particular translation by performing one additional 'side-translation'
	and comparing the result.
	The results of each test are then stored in a file.

	TODO: Handle 'None' cases
	"""
	def uniDirectionalTest(self, services, rows, target_language, origin_language = 'en'):
		# Get a language reference for the file being read.
		language_list = self._translation_file.getColumnNames('Google')

		for service in services:
			for row in rows:
				# Grab the direct translation from file.
				print('Retreiving direct translation..')
				direct_translation = self._translation_file.readCell(service, row, target_language)

				# Randomly select a side-language and grab its direct translation.
				print('Retreiving alternate translation..')
				random_language = random.choice([x for x in language_list if x != origin_language and x != target_language])	
				intermediate_translation = self._translation_file.readCell(service, row, random_language)

				# Translate this intermediate sentence into the same language as the direct translation.
				print('Performing Side Translation..')
				alternate_translation = self._translator.translate(service, intermediate_translation, target_language, random_language)

				# Compare the two translations.
				print('Comparing.. ', direct_translation, ' with ', alternate_translation)
				score = self.compare(direct_translation, alternate_translation)

				# Record the results.
				print('Recording Results..')
				original_phrase = self._translation_file.readCell(service, row, origin_language)  # Grab original phrase for records.
				self._results_file.appendEntry('Test Phrases', [service, original_phrase, origin_language, random_language, target_language, direct_translation, alternate_translation])
				self._results_file.appendEntry('Test Results', [service, origin_language, target_language, score['Lev-Distance']])

		print('Saving..')
		self._results_file.save()


	"""
	Compares two strings and returns a score based on their similarity.

	TODO: Incorporate more than one test result.
	"""
	def compare(self, phrase1, phrase2):
		return {'Lev-Distance': levenshteinDistance(phrase1, phrase2)['Ratio']}
