import re
import spacy,subprocess
from typing import Dict,List
import ssl,certifi
import nltk
import fitz
from nltk.corpus import stopwords

# This code snippet is checking if the 'stopwords' corpus is available in the nltk data. If it is not available, it will download the 'stopwords' corpus from the nltk website.

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    nltk.download('stopwords')

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    @staticmethod
    def clean_and_segment_text(text: str) -> str:
        text = re.sub(r'\(cid:\d+\)', ' ', text)
        text = text.replace('\r', ' ').replace('\t', ' ').replace('\xa0', ' ')

        headers = [
            "CAREER OBJECTIVE", "EDUCATION", "PROJECTS", "TECHNICAL SKILLS",
            "EXPERIENCE", "CERTIFICATIONS", "ACHIEVEMENTS", "EXTRACURRICULAR",
            "SUMMARY", "SKILLS"
        ]

        for header in headers:
            text = re.sub(
                rf'(?<!\n)(?<!^)(\.|\s)*({header})(\s|:|$)',
                rf'\n\2\n',
                text,
                flags=re.IGNORECASE
            )

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)

        return text.strip()
    @staticmethod
    def extract_links_from_pdf(pdf_path: str) -> dict:
        links = {"linkedin": "", "github": ""}

        with fitz.open(pdf_path) as doc:
            for page in doc:
                for link in page.get_links():
                    uri = link.get("uri", "")
                    if "linkedin.com/in" in uri:
                        links["linkedin"] = uri
                    elif "github.com" in uri:
                        links["github"] = uri

        return links
    def extract_sections(self, text: str) -> Dict[str, str]:
        sections = {
            'experience': '', 'education': '', 'skills': '', 'projects': '',
            'certifications': '', 'achievements': '', 'summary': '', 'extracurricular': ''
        }
        cleaned_text = self.clean_and_segment_text(text)
        cleaned_text = re.sub(
            r'(?<=\b)(CAREER OBJECTIVE|EDUCATION|PROJECTS|TECHNICAL SKILLS|CERTIFICATIONS|EXTRACURRICULAR|ACHIEVEMENTS|SKILLS|EXPERIENCE)(?=\b)',
            r'\n\1\n',
            cleaned_text,
            flags=re.IGNORECASE
        )
        lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]

        section_patterns = {
            'experience': r'\b(work\s*experience|professional\s*experience|employment\s*history|experience)\b',
            'education': r'\b(education|academic\s*background|qualifications)\b',
            'skills': r'\b(skills|technical\s*skills|core\s*competencies|technologies)\b',
            'summary': r'\b(summary|profile|objective|about\s*me|career\s*objective)\b',
            'projects': r'\b(projects|personal\s*projects)\b',
            'certifications': r'\b(certifications|certificates|licenses)\b',
            'achievements': r'\b(achievements|accomplishments|honors|awards|recognitions|key\s*achievements|notable\s*accomplishments)\b',
            'extracurricular': r'\b(extracurricular|activities)\b'
        }


        current_section = None
        HEADER_MAX_LENGTH = 60  # avoid false positives like long sentences

        # Step 3: Iterate through each line
        for line in lines:
            line_lower = line.lower()
            is_header = False

            # Check if the line looks like a section header
            if len(line) <= HEADER_MAX_LENGTH:
                for section, pattern in section_patterns.items():
                    if re.search(pattern, line_lower, re.IGNORECASE):
                        current_section = section
                        is_header = True
                        break

            # Skip the header line itself
            if is_header:
                continue

            # Append text to the current section
            if current_section:
                sections[current_section] += line + ' '
            else:
                # Default to summary if section not yet detected
                sections['summary'] += line + ' '

        # Step 4: Final cleanup
        for key in sections:
            sections[key] = sections[key].strip()

        return sections
    def extract_contact_info(self, text: str,pdf_path: str) -> Dict[str, str]:
        text = text.replace("\n", " ").replace("\r", " ")
        contact_info = {
            'email': '',
            'phone': '',
            'linkedin': '',
            'github': '',
        }
        email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]

        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\d{10}'
        phones = re.findall(phone_pattern, text)
        if phones:
            all_numbers = re.findall(r'\d{10}', text)
            if all_numbers:
                contact_info['phone'] = all_numbers[0]
            else:
                contact_info['phone'] = phones[0].strip()

        if pdf_path:
            from fitz import open as open_pdf
            with open_pdf(pdf_path) as doc:
                for page in doc:
                    for link in page.get_links():
                        uri = link.get("uri", "")
                        if "linkedin.com/in" in uri.lower():
                            contact_info["linkedin"] = uri
                        elif "github.com" in uri.lower():
                            contact_info["github"] = uri

        return contact_info

    
    def extract_years_of_experience(self, text: str) -> int:
        year_patterns = r'(19|20)\d{2}'
        years = re.findall(year_patterns, text)
        
        if not years:
            return 0
        
        years = [int(y) for y in years]
        if len(years) >= 2:
            return max(years) - min(years)
        
        return 0
    
    def tokenize_and_clean(self,text:str)->List[str]:
        doc=nlp(text.lower())

        tokens=[
            token.lemma_ for token in doc 
            if not token.is_stop
            and not token.is_punct
            and len(token.text)>2
        ]

        return tokens

    def extract_entities(self,text:str)->List[str]:
        doc=nlp(text)

        entities = {
            'organizations': [],
            'dates': [],
            'locations': [],
            'persons': []
        }
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'GPE':
                entities['locations'].append(ent.text)
            elif ent.label_ == 'PERSON':
                entities['persons'].append(ent.text)


