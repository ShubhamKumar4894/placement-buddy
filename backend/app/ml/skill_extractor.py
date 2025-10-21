import re
from typing import List, Dict

class SkillExtractor:
    TECHNICAL_SKILLS = {
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
        'go', 'golang', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'vue.js', 'node.js', 'express',
        'django', 'flask', 'fastapi', 'spring', 'asp.net', 'laravel',
        
        # Mobile Development
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'oracle', 'sqlite', 'cassandra', 'dynamodb',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
        'ci/cd', 'terraform', 'ansible', 'git', 'github', 'gitlab',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'nlp', 'computer vision', 'data analysis',
        'tableau', 'power bi', 'spark', 'hadoop',
        
        # Other
        'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira',
        'linux', 'bash', 'powershell', 'selenium', 'api', 'oauth'
    }
    
    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'problem solving', 
        'critical thinking', 'project management', 'time management',
        'collaboration', 'analytical', 'creative', 'adaptable', 'organized'
    }

    SKILL_ALIASES = {
        'js': 'javascript',
        'ts': 'typescript',
        'k8s': 'kubernetes',
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'cv': 'computer vision',
    }

    def __init__(self):
        self.technical_skills= {skill.lower() for skill in self.TECHNICAL_SKILLS}
        self.soft_skills= {skill.lower() for skill in self.SOFT_SKILLS}

    def extract_skills(self,text:str)->dict:

        text_lower=text.lower()
        found_technical_skills=set()
        found_soft_skills=set()

        for skill in self.technical_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_technical_skills.add(skill)

        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_soft_skills.add(skill)

        for alias, actual in self.SKILL_ALIASES.items():
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern,text_lower) and actual in self.technical_skills:
                found_technical_skills.add(actual)

        return {
            'technical_skills': sorted(list(found_technical_skills)),
            'soft_skills': sorted(list(found_soft_skills)),
            'all_skills': sorted(list(found_technical_skills.union(found_soft_skills)))
        }
    
    def extract_skills_from_section(self,skills_section:str)->List[str]:
        if not skills_section:
            return []
        
        skills= set()

        potential_skills=re.split(r'[,;|•\n]', skills_section)

        for item in potential_skills:
            item=item.strip().lower()

            if item in self.technical_skills or item in self.soft_skills:
                skills.add(item)
            
            for known_skill in self.technical_skills.union(self.soft_skills):
                if known_skill in item:
                    skills.add(known_skill)

        return sorted(list(skills))
    
    def categorize_skills(self,skills:List[str])->dict:

        categories = {
            'frontend': [],
            'backend': [],
            'mobile': [],
            'database': [],
            'cloud_devops': [],
            'data_science': [],
            'other': []
        }
        
        category_keywords = {
            'frontend': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'typescript'],
            'backend': ['python', 'java', 'node.js', 'django', 'flask', 'fastapi', 'spring', 'express'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd'],
            'data_science': ['machine learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'data analysis']
        }

        for skill in skills:
            categorized=False
            for category, keywords in category_keywords.items():
                if skill in keywords:
                    categories[category].append(skill)
                    categorized=True
                    break
            
            if not categorized:
                categories['other'].append(skill)

        return {k: v for k, v in categories.items() if v}
    
    def count_skill_mentions(self, text: str, skill: str) -> int:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        return len(re.findall(pattern, text.lower()))


