from EGPT import db
from app import app
from EGPT.models import Service, Tutorial

app.app_context().push()

# Example function for inserting tutorials
def insert_tutorials():
    tutorials = {
        'Vocabulary Mastery': [
            {'title': 'Vocabulaary Basics', 'video_url': 'https://www.youtube.com/embed/EFyxC_uI9lg?si=A2zUNHCLfN5E9k6x'},
            {'title': '20 English words with meaning', 'video_url': 'https://www.youtube.com/embed/8YYQ7cYRo7Q?si=vEZtiQ7vVA3s4o0K'},
            {'title': 'Root word GYNE', 'video_url': 'https://www.youtube.com/embed/OHcHk5__gCQ?si=ZV2P7quyOjFspjlF'},
            {'title': 'Root word ANDROS', 'video_url': 'https://www.youtube.com/embed/KiEp_08yxAw?si=Ea5V2rEa6BhQyHTa'},
            {'title': 'Doctors who are specialist', 'video_url': 'https://www.youtube.com/embed/KiEp_08yxAw?si=H9evRpoqWP-9UydH'},
            {'title': 'Murders and Killing', 'video_url': 'https://www.youtube.com/embed/KiEp_08yxAw?si=XG8CfEMC7CDyOkR_'},
            {'title': 'Hands on feet', 'video_url': 'https://www.youtube.com/embed/oXKS7npr_JE?si=KeIoZN7T6HBAIDcq'},
            {'title': 'Good and bad', 'video_url': 'https://www.youtube.com/embed/xYZvJor-9eA?si=25X_lbdqvoB7rrHz'},
            {'title': 'Human kind', 'video_url': 'https://www.youtube.com/embed/jW7wacTEyyU?si=jwJUXSb2TIa1F9cF'}
        ],
        'Grammar Essentials': [
            {'title': 'Nouns','video_url': 'https://www.youtube.com/embed/8IogxPUrW7k?si=jnAQ7COoSuX2XVBl'},
            {'title': 'Singular and plural nouns', 'video_url': 'https://www.youtube.com/embed/F8M6MxypjEo?si=thKS-iqe2YmCereP'},
            {'title': 'Irregular plural Nouns', 'video_url': 'https://www.youtube.com/embed/ehCrFcFxfVo?si=_82hGE4KMilGNSe7'},
            {'title': 'Compound Nouns', 'video_url': 'https://www.youtube.com/embed/IaUmrzUPU1k?si=UtPSa0p6pG0D1ili'},
            {'title': 'Countable and uncountable Nouns', 'video_url': 'https://www.youtube.com/embed/rS5rfMJvwK4?si=SXKxvhN7WzX2rnf6'},
            {'title': 'Adjectives 1', 'video_url': 'https://www.youtube.com/embed/S3ChAWSu4L4?si=JOYpJe0VYN4xf_bF'},
            {'title': 'Adjectives 2: Prefixes and suffixes', 'video_url': 'https://www.youtube.com/embed/aET7ax8UM3w?si=lV4d11XNIK_OZfmV'},
            {'title': 'Adjectives 3', 'video_url': 'https://www.youtube.com/embed/P3TsNBGjBWk?si=GPi5_LpGpkgBDy1C'},
            {'title': 'Adjectives 4', 'video_url': 'https://www.youtube.com/embed/ibdtKYnWP1Q?si=_2T_iyQySQ_heU18'},
            {'title': 'Adjectives 5', 'video_url': 'https://www.youtube.com/embed/E-YYxdv_U0c?si=YFYBDAFPO7m2d134'}
        ],
        'Speaking Fluency': [
            {'title': 'Improve your SPEAKING and CONVERSATIONAL skills #1','video_url': 'https://www.youtube.com/embed/0r0h5hvwq-A?si=d5-YPG-cPMt0ibyL'},
            {'title': 'Improve your Speaking and Conversational skills #2', 'video_url': 'https://www.youtube.com/embed/aRBzYEn7dhM?si=cQMQGEo5DrPd9OFd'},
            {'title': 'Improve your Speaking and Conversational #3', 'video_url': 'https://www.youtube.com/embed/ehCrFcFxfVo?si=_82hGE4KMilGNSe7'},
            {'title': 'Improve your Speaking this simple method', 'video_url': 'https://www.youtube.com/embed/-QoYVG14a9A?si=iGyvmgU7Ey2b6KRQ'},
            {'title': 'Improve your Speaking and Conversational  #4', 'video_url': 'https://www.youtube.com/embed/7BXlrH1ZpBA?si=YOhDuVzL5S67yE1Z'},
            {'title': 'Improve your Speaking and Conversational  #5', 'video_url': 'https://www.youtube.com/embed/Cw15K8_z-b4?si=TwLMHDVh0_MktG2E'},
            {'title': '5 min DAILY exercises', 'video_url': 'https://www.youtube.com/embed/tiyfUZFLDm4?si=pqrN5tcU91suf3tH'},
            {'title': 'Improve your Speaking and Conversational skills #6', 'video_url': 'https://www.youtube.com/embed/xpINY3bleUQ?si=TZngTiap8mNJ9aNA'},
            {'title': 'Improve your Speaking and Conversational skills #7', 'video_url': 'https://www.youtube.com/embed/OItW5ONQfrk?si=poMp_mEx3Khd_YVW'},
            {'title': 'Improve your Speaking and Conversational skills #8', 'video_url': 'https://www.youtube.com/embed/QdDNdbkeo5U?si=yyU2repC-XP0u8ug'}
        ],
        'Listening Skills': [
            {'title': 'Listening Comprehension Level 1 Lesson 1','video_url': 'https://www.youtube.com/embed/_r9pWWYjBFw?si=6wpzIfMnsFiHTpXU'},
            {'title': 'Listening Comprehension Level 1 Lesson 2', 'video_url': 'https://www.youtube.com/embed/wyQ2_KRzffU?si=HyD6ubf9Z-L9a4eH'},
            {'title': 'Listening Comprehension Level 1 Lesson 3', 'video_url': 'https://www.youtube.com/embed/UYEANkxhn8g?si=gGbR7uM7fEhDVosX'},
            {'title': 'Listening Comprehension Level 1 Lesson 4', 'video_url': 'https://www.youtube.com/embed/U4zivrfY0LE?si=_OYQ6MfMp7dto3Tg'},
            {'title': 'Listening Comprehension Level 1 Lesson 5', 'video_url': 'https://www.youtube.com/embed/SCZSLh-6GGk?si=Doi8oXgJkaSgBwhs'},
            {'title': 'Listening Comprehension Level 1 Lesson 6', 'video_url': 'https://www.youtube.com/embed/i2X6C4_v7k8?si=uCl5STxB7R6i5pG4'},
            {'title': 'Listening Comprehension Level 1 Lesson 7', 'video_url': 'https://www.youtube.com/embed/SYc6WhlfJ1g?si=i4wEfRSPhej9slNM'},
            {'title': 'Listening Comprehension Level 1 Lesson 8', 'video_url': 'https://www.youtube.com/embed/XV4kgUrDKCY?si=Nz4-vE4mk85Bsi-M'},
            {'title': 'Listening Comprehension Level 1 Lesson 9', 'video_url': 'https://www.youtube.com/embed/EVrRVE1KCxs?si=cPHs9_PP4OeQxx7R'},
            {'title': 'Listening Comprehension Level 1 Lesson 10', 'video_url': 'https://www.youtube.com/embed/rhjBPvBKYWg?si=HKcSXeKo-qNsl8DA'},
            {'title': 'Listening Comprehension Level 1 Lesson 11', 'video_url': 'https://www.youtube.com/embed/lNR6mdQIV0c?si=8nW4JIFoM4UNV8GT'},
            {'title': 'Listening Comprehension Level 1 Lesson 12', 'video_url': 'https://www.youtube.com/embed/l5B6z14y_Ac?si=N1CGPq5Du1EJz3Kf'},
            {'title': 'Listening Comprehension Level 1 Lesson 13', 'video_url': 'https://www.youtube.com/embed/kxLazb3vVys?si=lMb18trwEwH7Ctdc'}
        ],
        'Writing Proficiency': [
            {'title': 'Grammar Lesson #1 - Tips to Improve Your Sentence Structure','video_url': 'https://www.youtube.com/embed/Drv6jD8xWdw?si=X_U92D-NoIm9QXD_'},
            {'title': 'Emails in English - How to Write an Email in English', 'video_url': 'https://www.youtube.com/embed/xay5TeJVSC0?si=FccuMDRcmIvWCoj4'},
            {'title': 'English Punctuation Guide', 'video_url': 'https://www.youtube.com/embed/gfYq2ng9s4E?si=-HQAn55e46ESZUNl'},
            {'title': 'How to Improve Your English Writing', 'video_url': 'https://www.youtube.com/embed/VgTqZOZ1UMQ?si=fiKpphOzclkjJe8d'},
            {'title': 'English Spelling Rules - Learn Spelling Rules and Common Mistakes', 'video_url': 'https://www.youtube.com/embed/IWPfD2WcAXg?si=9hQ9gplEbKS-IZuL'},
            {'title': 'IELTS Essay - Tips to Write a Good IELTS Writing Task 2 Essay', 'video_url': 'https://www.youtube.com/embed/HR7YE7oDWCE?si=ntGcPnvd-0nOaREm'},
            {'title': 'IELTS Writing - Using Linking Words and Phrases to Improve Your Score', 'video_url': 'https://www.youtube.com/embed/OsWmxQfyG8k?si=v53REKLjwjHwC5iD'},
            {'title': 'How To Use Commas ', 'video_url': 'https://www.youtube.com/embed/tNKBut921qM?si=ztE6zjD1iqVASyxK'},
            {'title': '5 Ways to Compare and Contrast in English', 'video_url': 'https://www.youtube.com/embed/EOsxooAh9_4?si=CfiPp2DU_SHnjfZY'},
            {'title': 'Complex Sentences in English Writing - Learn How to Make Complex Sentences', 'video_url': 'https://www.youtube.com/embed/W-uPiTB877c?si=dCq9sN2JO3IZRcRd'}
        ],
        'Reading Comprehension': [
            {'title': 'Introduction','video_url': 'https://www.youtube.com/embed/ZNq2JHEd0HE?si=cxpXtuZ-DkNx60Oy'},
            {'title': 'Article Based Passage - 1', 'video_url': 'https://www.youtube.com/embed/4X26f20r-aE?si=ltnbV6JL_5_wUuam'},
            {'title': 'Article Based Passage - 2 ', 'video_url': 'https://www.youtube.com/embed/YcWleBmLDBc?si=upHVPpAPqkxP1vfe'},
            {'title': 'Article Based Passage - 3', 'video_url': 'https://www.youtube.com/embed/oMce7VJgmbQ?si=3aCTiMBv9nievN_D'},
            {'title': 'Story Based Passage - 1', 'video_url': 'https://www.youtube.com/embed/haBgUSnwIBw?si=RUyt83IKAPr1u0sc'},
            {'title': 'Story Based Passage - 2 ', 'video_url': 'https://www.youtube.com/embed/u7s01kfugkE?si=h34y-7UtLx6TB1lu'},
            {'title': 'Story Based Passage - 3', 'video_url': 'https://www.youtube.com/embed/XWQHgFv-n5Y?si=EqPnGRXjxz--Vda8'},
            {'title': 'Short Passage - 1', 'video_url': 'https://www.youtube.com/embed/nvwYVzbu6FM?si=uf24M_8nV1b_XK9R'},
            {'title': 'Short Passage - 2 ', 'video_url': 'https://www.youtube.com/embed/zBKtGL3iKVo?si=72a1UTTno0dezvdm'},
            {'title': 'Short Passage - 3', 'video_url': 'https://www.youtube.com/embed/04XpRSx_fdU?si=hyl1JZSolQl0X0ZM'}
        ]
    }
    # Insert tutorials into the database
    for service_name, tutorial_list in tutorials.items():
        # Assuming you already have Service entries in the database
        service = Service.query.filter_by(name=service_name).first()
        if service:
            for tutorial_data in tutorial_list:
                new_tutorial = Tutorial(
                    title=tutorial_data['title'],
                    video_url=tutorial_data['video_url'],
                    service_id=service.id
                )
                db.session.add(new_tutorial)
    db.session.commit()

insert_tutorials()
