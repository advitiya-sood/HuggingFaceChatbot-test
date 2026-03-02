from src.search import AdvancedRAGPipeline
import time

questions = [
    "What is the process to apply Paid Leave?",
    "What is the process to avail paternity leaves?",
    "What is the process for availing parental insurance?",
    "My PF Contribution for Jan 2026 month is not credited and visible in PF portal.",
    "How I can claim medical reimbursement?",
    "How can I change address & bank details in Adrenalin HRMS?",
    "How should I regularize attendance in portal?",
    "What are the minimum hours required to mark full day present?",
    "What is the eligibility of shift allowances?",
    "What are the dates for salary credit?",
    "I want to file complaint on POSH, what is the process?",
    "What is the appraisal process?",
    "What is the loan policy?",
    "What is the policy on sabbatical leaves?",
    "AS per the company records, I noticed that there is a mismatch in my total years of working experience. I mentioned the same in my Resume as well. Please recheck and update the records accordingly to reflect the accurate details.\n\nPlease let me know if you require any documentary evidence.\n\nI started my career on 15th Feb 2010.",
    "I'm unable to do the biometric attendance as i'm having mehandi to my hands",
    "Currently My RM is showing as Santosh Kumar and my other team members like Shahid, Vyshnavi are having Saleemuddin Mewati as their RM. My RM should be either Saleemuddin Mewati or Ashok Kumar. please update this.",
    "I got married recently and request to add my wife to my Health Insurance e-card. I also request to include my father and mother as dependents. will provide the required documents. Kindly process the request.",
    "Change RM of Shruthik Ravula to Rohan Kakkar and so does in IT System like Teams and Outlook etc..",
    "Dear HR Team,\n\nSandeep Kumar Verma (EMP ID: 666) has applied for a one-day leave on January 2nd in the ADL system. However, I am unable to view this request on my end for approval. Could you please check and take the necessary action so that the request becomes visible for my approval?\nThank you for your support.",
    "Dear HR Team,\nI am reaching out regarding the leave availed report shared with Uno recently. I noticed a discrepancy between the number of leaves I have availed and what is reflected in the report. As per my records, I have availed 12 days of leave this year, whereas the report indicates 17 days.\nCould you kindly review attached leave availed from the ADL tool and make the necessary corrections? \nThank you for your assistance.\nThanks and Regards, Ajay Kumar Singh",
    "PF amount is deducted but it's not reflecting my payslip and also no pf account number is added in my pay slip",
    "As per the recent salary increment updates, my experience still appears incorrect in the records. I had earlier raised Ref No: HR_BS-CR50_1016, which was closed with the assurance of updating this detail. \n\nAdditionally, having completed 2.6 years with Bhavna and currently handling responsibilities aligned with a Product Owner, I’d be grateful if you could advise on the process and criteria for a title upgradation.\n\nAppreciate if company can consider the above points for salary review."
]

def main():
    rag = AdvancedRAGPipeline()
    output_lines = ["# Chatbot FAQ Responses\n\nHere are the chatbot's responses to the 23 frequently asked questions:\n\n---\n"]
    
    for i, q in enumerate(questions, 1):
        print(f"Processing question {i}/{len(questions)}...")
        try:
            # Add a small delay to avoid hitting LLM API rate limits globally if any
            time.sleep(1)
            res = rag.query(q, top_k=5)
            ans = res['answer']
        except Exception as e:
            ans = f"Error generating answer: {e}"
            
        # Clean up the output string a bit
        output_lines.append(f"### Ques. {i}) {q}")
        output_lines.append(f"**Chatbot Response:**\n{ans}\n")
        output_lines.append("---\n")

    with open("faq_responses.md", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
        
    print("Done! Saved to faq_responses.md")

if __name__ == '__main__':
    main()
