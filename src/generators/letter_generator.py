"""
Letter Generator Module
Generates cover letters, motivation letters, and follow-up emails
"""

from datetime import datetime
from typing import Dict, List, Optional


class LetterGenerator:
    """Generates professional letters for job applications"""

    def __init__(self):
        self.letter_templates = self._load_templates()
        self.tone_styles = {
            "formal": {
                "greeting": "Dear",
                "closing": "Yours sincerely",
                "style": "professional and formal"
            },
            "professional": {
                "greeting": "Dear",
                "closing": "Best regards",
                "style": "professional and approachable"
            },
            "casual": {
                "greeting": "Hi",
                "closing": "Kind regards",
                "style": "friendly and professional"
            }
        }

    def _load_templates(self) -> Dict:
        """Load letter templates"""
        return {
            "cover_letter": {
                "sections": ["header", "opening", "body", "skills", "motivation", "closing"],
                "max_length": 400
            },
            "motivation_letter": {
                "sections": ["header", "opening", "background", "motivation", "goals", "closing"],
                "max_length": 500
            },
            "follow_up": {
                "sections": ["greeting", "reference", "interest", "availability", "closing"],
                "max_length": 200
            },
            "thank_you": {
                "sections": ["greeting", "gratitude", "highlights", "next_steps", "closing"],
                "max_length": 150
            }
        }

    def generate_cover_letter(
        self,
        cv_data: Dict,
        job_data: Dict,
        match_analysis: Optional[Dict] = None,
        tone: str = "professional",
        custom_points: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate a tailored cover letter
        
        Args:
            cv_data: Parsed CV data
            job_data: Parsed job description data
            match_analysis: Optional match analysis results
            tone: Letter tone (formal, professional, casual)
            custom_points: Custom points to emphasize
            
        Returns:
            Dict with letter content and metadata
        """
        tone_config = self.tone_styles.get(tone, self.tone_styles["professional"])
        
        letter = {
            "type": "cover_letter",
            "date": datetime.now().strftime("%B %d, %Y"),
            "tone": tone,
            "sections": {}
        }

        # Header section
        letter["sections"]["header"] = self._generate_header(cv_data, job_data)

        # Opening paragraph
        letter["sections"]["opening"] = self._generate_opening(
            job_data, 
            tone_config
        )

        # Body - Why you're a good fit
        letter["sections"]["body"] = self._generate_body(
            cv_data,
            job_data,
            match_analysis
        )

        # Skills section
        letter["sections"]["skills"] = self._generate_skills_section(
            cv_data,
            job_data,
            match_analysis
        )

        # Motivation
        letter["sections"]["motivation"] = self._generate_motivation(
            job_data,
            custom_points
        )

        # Closing
        letter["sections"]["closing"] = self._generate_closing(tone_config)

        # Compile full text
        letter["full_text"] = self._compile_letter(letter["sections"])
        letter["word_count"] = len(letter["full_text"].split())

        return letter

    def generate_motivation_letter(
        self,
        cv_data: Dict,
        program_data: Dict,
        personal_statement: Optional[str] = None,
        tone: str = "formal"
    ) -> Dict:
        """Generate a motivation letter for academic programs or special positions"""
        tone_config = self.tone_styles.get(tone, self.tone_styles["formal"])
        
        letter = {
            "type": "motivation_letter",
            "date": datetime.now().strftime("%B %d, %Y"),
            "tone": tone,
            "sections": {}
        }

        letter["sections"]["header"] = self._generate_header(cv_data, program_data)
        letter["sections"]["opening"] = self._generate_academic_opening(program_data, tone_config)
        letter["sections"]["background"] = self._generate_background(cv_data)
        letter["sections"]["motivation"] = personal_statement or self._generate_personal_motivation(program_data)
        letter["sections"]["goals"] = self._generate_goals(program_data)
        letter["sections"]["closing"] = self._generate_closing(tone_config)

        letter["full_text"] = self._compile_letter(letter["sections"])
        letter["word_count"] = len(letter["full_text"].split())

        return letter

    def generate_follow_up_email(
        self,
        job_data: Dict,
        application_date: str,
        interview_date: Optional[str] = None,
        tone: str = "professional"
    ) -> Dict:
        """Generate a follow-up email after application or interview"""
        tone_config = self.tone_styles.get(tone, self.tone_styles["professional"])
        
        email = {
            "type": "follow_up",
            "date": datetime.now().strftime("%B %d, %Y"),
            "tone": tone,
            "subject": f"Following up on {job_data.get('title', 'Application')} Application",
            "sections": {}
        }

        email["sections"]["greeting"] = f"{tone_config['greeting']} Hiring Manager,"
        
        if interview_date:
            email["sections"]["reference"] = self._generate_post_interview_reference(
                job_data,
                interview_date
            )
        else:
            email["sections"]["reference"] = self._generate_application_reference(
                job_data,
                application_date
            )

        email["sections"]["interest"] = self._generate_continued_interest(job_data)
        email["sections"]["availability"] = self._generate_availability_statement()
        email["sections"]["closing"] = self._generate_email_closing(tone_config)

        email["full_text"] = self._compile_email(email["sections"])
        email["word_count"] = len(email["full_text"].split())

        return email

    def generate_thank_you_email(
        self,
        job_data: Dict,
        interviewer_name: Optional[str] = None,
        interview_highlights: Optional[List[str]] = None,
        tone: str = "professional"
    ) -> Dict:
        """Generate a thank you email after an interview"""
        tone_config = self.tone_styles.get(tone, self.tone_styles["professional"])
        
        email = {
            "type": "thank_you",
            "date": datetime.now().strftime("%B %d, %Y"),
            "tone": tone,
            "subject": f"Thank You - {job_data.get('title', 'Interview')} Interview",
            "sections": {}
        }

        greeting_name = interviewer_name or "Hiring Manager"
        email["sections"]["greeting"] = f"{tone_config['greeting']} {greeting_name},"

        email["sections"]["gratitude"] = self._generate_gratitude(job_data)
        email["sections"]["highlights"] = self._generate_interview_highlights(
            job_data,
            interview_highlights
        )
        email["sections"]["next_steps"] = self._generate_next_steps()
        email["sections"]["closing"] = self._generate_email_closing(tone_config)

        email["full_text"] = self._compile_email(email["sections"])
        email["word_count"] = len(email["full_text"].split())

        return email

    def customize_letter(
        self,
        base_letter: Dict,
        customizations: Dict
    ) -> Dict:
        """Apply customizations to a generated letter"""
        customized = base_letter.copy()
        
        for section, content in customizations.items():
            if section in customized["sections"]:
                customized["sections"][section] = content
        
        customized["full_text"] = self._compile_letter(customized["sections"])
        customized["word_count"] = len(customized["full_text"].split())
        customized["customized"] = True
        
        return customized

    # Helper methods for generating content

    def _generate_header(self, cv_data: Dict, target_data: Dict) -> str:
        """Generate letter header with contact information"""
        name = cv_data.get("name", "Your Name")
        email = cv_data.get("email", "your.email@example.com")
        phone = cv_data.get("phone", "")
        
        company = target_data.get("company", "Company Name")
        
        header = f"{name}\n"
        if email:
            header += f"{email}\n"
        if phone:
            header += f"{phone}\n"
        header += f"\n{datetime.now().strftime('%B %d, %Y')}\n\n"
        header += f"{company}\n"
        
        return header

    def _generate_opening(self, job_data: Dict, tone_config: Dict) -> str:
        """Generate opening paragraph"""
        position = job_data.get("title", "the position")
        company = job_data.get("company", "your company")
        
        opening = f"{tone_config['greeting']} Hiring Manager,\n\n"
        opening += f"I am writing to express my strong interest in the {position} position at {company}. "
        opening += f"With my background and skills, I am confident I would be a valuable addition to your team."
        
        return opening

    def _generate_body(
        self,
        cv_data: Dict,
        job_data: Dict,
        match_analysis: Optional[Dict]
    ) -> str:
        """Generate main body highlighting relevant experience"""
        body = "In my current role, I have developed strong expertise in "
        
        if match_analysis and "matching_skills" in match_analysis:
            skills = match_analysis["matching_skills"][:3]
            body += ", ".join(skills) + ". "
        else:
            skills = cv_data.get("skills", [])[:3]
            body += ", ".join(skills) + ". "
        
        body += "My experience directly aligns with your requirements, "
        body += "and I am excited about the opportunity to contribute to your team's success."
        
        return body

    def _generate_skills_section(
        self,
        cv_data: Dict,
        job_data: Dict,
        match_analysis: Optional[Dict]
    ) -> str:
        """Generate skills highlight section"""
        skills_text = "Key qualifications I bring include:\n"
        
        if match_analysis and "matching_skills" in match_analysis:
            skills = match_analysis["matching_skills"][:4]
        else:
            required = job_data.get("required_skills", [])
            cv_skills = cv_data.get("skills", [])
            skills = [s for s in cv_skills if s in required][:4]
        
        for skill in skills:
            skills_text += f"• {skill}\n"
        
        return skills_text

    def _generate_motivation(
        self,
        job_data: Dict,
        custom_points: Optional[List[str]]
    ) -> str:
        """Generate motivation section"""
        company = job_data.get("company", "your organization")
        
        motivation = f"I am particularly drawn to {company} because of "
        
        if custom_points:
            motivation += ", ".join(custom_points) + ". "
        else:
            motivation += "your reputation for innovation and excellence in the industry. "
        
        motivation += "I am eager to bring my skills and enthusiasm to your team."
        
        return motivation

    def _generate_closing(self, tone_config: Dict) -> str:
        """Generate closing paragraph"""
        closing = "Thank you for considering my application. "
        closing += "I look forward to the opportunity to discuss how I can contribute to your team. "
        closing += "I am available for an interview at your convenience.\n\n"
        closing += f"{tone_config['closing']},\n"
        closing += "[Your Name]"
        
        return closing

    def _generate_academic_opening(self, program_data: Dict, tone_config: Dict) -> str:
        """Generate opening for academic motivation letter"""
        program = program_data.get("program_name", "the program")
        institution = program_data.get("institution", "your institution")
        
        opening = f"{tone_config['greeting']} Selection Committee,\n\n"
        opening += f"I am writing to apply for {program} at {institution}. "
        opening += "I am deeply passionate about this field and believe this program "
        opening += "aligns perfectly with my academic and professional goals."
        
        return opening

    def _generate_background(self, cv_data: Dict) -> str:
        """Generate academic/professional background section"""
        education = cv_data.get("education", [])
        
        background = "My academic journey has prepared me well for this opportunity. "
        
        if education:
            latest = education[0]
            degree = latest.get("degree", "degree")
            field = latest.get("field", "field")
            background += f"I hold a {degree} in {field}, "
            background += "where I developed strong analytical and problem-solving skills."
        
        return background

    def _generate_personal_motivation(self, program_data: Dict) -> str:
        """Generate personal motivation statement"""
        program = program_data.get("program_name", "this program")
        
        motivation = f"I am motivated to pursue {program} because "
        motivation += "I believe it will provide me with the knowledge and skills "
        motivation += "necessary to make meaningful contributions to the field. "
        motivation += "My long-term goal is to apply what I learn to address real-world challenges."
        
        return motivation

    def _generate_goals(self, program_data: Dict) -> str:
        """Generate future goals section"""
        goals = "Upon completion of this program, I aim to "
        goals += "leverage my enhanced expertise to drive innovation and contribute "
        goals += "to advancing the field. I am committed to continuous learning "
        goals += "and professional development."
        
        return goals

    def _generate_application_reference(self, job_data: Dict, application_date: str) -> str:
        """Generate reference to previous application"""
        position = job_data.get("title", "the position")
        
        reference = f"I recently applied for the {position} position on {application_date}. "
        reference += "I wanted to follow up and reiterate my strong interest in this opportunity."
        
        return reference

    def _generate_post_interview_reference(self, job_data: Dict, interview_date: str) -> str:
        """Generate reference to interview"""
        position = job_data.get("title", "the position")
        
        reference = f"Thank you for the opportunity to interview for the {position} position on {interview_date}. "
        reference += "I enjoyed our conversation and learning more about the role and your team."
        
        return reference

    def _generate_continued_interest(self, job_data: Dict) -> str:
        """Generate statement of continued interest"""
        company = job_data.get("company", "your organization")
        
        interest = f"I remain very interested in joining {company} and contributing to your team. "
        interest += "I believe my skills and experience would be a great match for this role."
        
        return interest

    def _generate_availability_statement(self) -> str:
        """Generate availability statement"""
        return "I am happy to provide any additional information you may need and am available for further discussion at your convenience."

    def _generate_gratitude(self, job_data: Dict) -> str:
        """Generate gratitude statement"""
        position = job_data.get("title", "the position")
        
        gratitude = f"Thank you for taking the time to meet with me regarding the {position} role. "
        gratitude += "I truly appreciated the opportunity to learn more about your team and the exciting work you're doing."
        
        return gratitude

    def _generate_interview_highlights(
        self,
        job_data: Dict,
        highlights: Optional[List[str]]
    ) -> str:
        """Generate interview highlights section"""
        text = "Our discussion reinforced my enthusiasm for this opportunity. "
        
        if highlights:
            text += "I was particularly excited to learn about "
            text += " and ".join(highlights) + ". "
        
        text += "I am confident that my background and skills align well with your needs."
        
        return text

    def _generate_next_steps(self) -> str:
        """Generate next steps statement"""
        return "I look forward to hearing about the next steps in your hiring process. Please don't hesitate to reach out if you need any additional information."

    def _generate_email_closing(self, tone_config: Dict) -> str:
        """Generate email closing"""
        closing = f"\n{tone_config['closing']},\n"
        closing += "[Your Name]"
        
        return closing

    def _compile_letter(self, sections: Dict) -> str:
        """Compile letter sections into full text"""
        return "\n\n".join(sections.values())

    def _compile_email(self, sections: Dict) -> str:
        """Compile email sections into full text"""
        return "\n\n".join(sections.values())

    def validate_letter(self, letter: Dict) -> Dict:
        """Validate letter quality and completeness"""
        validation = {
            "valid": True,
            "issues": [],
            "suggestions": []
        }

        # Check word count
        word_count = letter.get("word_count", 0)
        letter_type = letter.get("type", "cover_letter")
        max_length = self.letter_templates[letter_type]["max_length"]
        
        if word_count > max_length:
            validation["issues"].append(f"Letter exceeds recommended length ({word_count}/{max_length} words)")
            validation["valid"] = False
        
        if word_count < 100:
            validation["issues"].append("Letter is too short")
            validation["valid"] = False

        # Check for required sections
        required_sections = self.letter_templates[letter_type]["sections"]
        missing_sections = [s for s in required_sections if s not in letter["sections"]]
        
        if missing_sections:
            validation["issues"].append(f"Missing sections: {', '.join(missing_sections)}")
            validation["valid"] = False

        return validation
