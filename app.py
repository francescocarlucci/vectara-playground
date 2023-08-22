import json
import requests
import streamlit as st

st.set_page_config(
    page_title="Vectara Playground",
    page_icon="⚡"
)

st.header('⚡ Vectara Playground')

st.success("This is a demo project related to the [Learn LangChain](https://learnlangchain.org/) mini-course.")

st.write('''
Vectara is vector database solution that simplifies the process of indexing and semantically searching
different types of documents (even of significant size) through a simple and convenient API. With this
"playground", you can familiarize with the Vectara API, format and debug the payload editing the most
important parameters via the interface, and see the results of your search queries. 
''')

st.write('''
Of course, before running queries you have to:

- sign up to Vectara.com
- create a "corpus" (it's Vectara's way to name document containers)
- upload documents to your Corpus
- create an API key
''')

st.write('''
Document uploading/indexing can also be done via API, maybe that will be the next step for this little playground :)
''')

st.info("You need your own Vectara keys. The form will process your keys safely and never store them anywhere.", icon="🔒")

vectara_api_key = st.text_input("Vectara API Key")

col1, col2 = st.columns(2)

with col1:
	vectara_customer_id = st.text_input("Vectara Customer Id")

with col2:
	vectara_corpus_id = st.text_input("Vectara Corpus Id")

col1, col2, col3, col4 = st.columns(4)

with col1:
	num_results = st.number_input("Number of results to return", min_value=1, max_value=10, value=2, step=1)

with col2:
	chars_before = st.number_input("Chars before", min_value=10, max_value=100, value=30, step=1)
	sentences_before = st.number_input("Sentences before", min_value=1, max_value=10, value=3, step=1)

with col3:
	chars_after = st.number_input("Chars after", min_value=10, max_value=100, value=30, step=1)
	sentences_after = st.number_input("Sentences after", min_value=1, max_value=10, value=3, step=1)

with col4:
	max_summarized_results = st.number_input("Max summarized results", min_value=1, max_value=10, value=3, step=1)
	summary_language = st.selectbox(
	'Summary Language',
	('en', 'es', 'fr'))

query = st.text_input("Your search query:")

response_type = st.selectbox(
	'Response type',
	('full', 'summary'))

debug_payload = st.checkbox('Debug Payload')

with st.form("vectara_playground"):

	payload = {
		"query": [
			{
				"query": query,
				"start": 0,
				"numResults": num_results,
				"contextConfig": {
					"charsBefore": chars_before,
					"charsAfter": chars_after,
					"sentencesBefore": sentences_before,
					"sentencesAfter": sentences_after,
					#"startTag": "<b>",
					#"endTag": "</b>",
				},
				"corpusKey": [
					{
						"customerId": vectara_customer_id,
						"corpusId": vectara_corpus_id,
						"semantics": "DEFAULT",
						#"dim": [{"name": "string", "weight": 0}],
						#"metadataFilter": "",
						#"lexicalInterpolationConfig": {"lambda": 0},
					}
				],
				"rerankingConfig": {"rerankerId": 272725717},
				"summary": [
					{
						"summarizerPromptName": "vectara-summary-ext-v1.2.0",
						"maxSummarizedResults": max_summarized_results,
						"responseLang": summary_language,
					}
				],
			}
		]
	}

	if debug_payload:
		st.write(payload)

	search = st.form_submit_button("🚀 Run the Search")

	if search:

		with st.spinner('Processing your request...'):

			api_url = "https://api.vectara.io/v1/query"

			payload = json.dumps(payload)

			headers = {
				'Content-Type': 'application/json',
				'Accept': 'application/json',
				'customer-id': vectara_customer_id,
				'x-api-key': vectara_api_key
			}

			response = requests.request("POST", api_url, headers=headers, data=payload)

			results = json.loads(response.text)

			if response_type == 'summary':

				summary = results['responseSet'][0]['summary'][0]['text']

				st.write(summary)

			else:

				st.write(results)

st.divider()

st.write('A project by [Francesco Carlucci](https://francescocarlucci.com) - \
Need AI training / consulting? [Get in touch](mailto:info@francescocarlucci.com)')