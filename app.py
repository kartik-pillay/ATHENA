import flask
from flask import render_template, request,jsonify
from flask_cors import CORS
app = flask.Flask(__name__)

# Define keywords and their corresponding problems
keyword_to_problem = {
    "boss": "boss",
    "exam": "exam preparation",
    "time management": "time management",
    "managing my time": "time management",
    "annoying": "boss",
    "bothering me": "boss",
    "care giver": "care giver",
    "pregnancy": "post partum",
    "care": "care giver",
    "missing my home": "home sick",
    "assignment": "assignment",
    "deadline": "assignment",
    "distracted": "d_s",
    "not able to focus": "d_s",
}

# Define structured data with solutions for each problem
structured_data = {
    "career stress": {
        "unemployed": ["Solution G", "Solution H", "Solution I"],
        "work stress": ["Solution J", "Solution K", "Solution L"],
        "boss": ["Solution X", "Solution Y", "Solution Z"],
        "house wife": ["Solution D", "Solution E", "Solution F"],
    },
    "academic stress": {
        "exam preparation": [
            "I understand that exams can be stressful. To help manage your stress, consider incorporating relaxation techniques into your daily routine. Deep breathing exercises, mindfulness meditation, and short walks can be effective ways to reduce anxiety and improve focus.",
            "As your exams approach, it's helpful to practice past exams or questions under timed conditions. This will familiarize you with the format of the questions and help you develop strategies for managing your time during the test. Don't forget to stay organized and stay calm during the exam.",
            "To tackle your upcoming exams with confidence, it's essential to employ effective study techniques. Try active learning, summarization, and practice problems to reinforce your understanding of the material. Consistent practice and varied study materials can make a significant difference in your performance.",
        ],
        "time management": [
            "Consider adopting time blocking and scheduling techniques. Allocate specific time slots for classes, assignments, and personal activities. Stick to your schedule to ensure a balanced workload and reduce stress.",
            "Take advantage of college resources, such as academic advisors and study groups. Academic advisors can assist you in planning your courses and workload. Joining study groups can help you share the workload and receive support from peers.",
            "Remember to prioritize self-care. Incorporate stress reduction techniques like mindfulness, deep breathing, or short breaks. Maintaining a healthy work-life balance is crucial for reducing stress and maintaining well-being.",
        ],
        "home sick": [
            "I understand that missing home and struggling with social adjustment can be challenging. To cope with homesickness, try staying connected with your family through regular calls and video chats. As for making friends, consider joining clubs or groups related to your interests. Engaging in activities you enjoy can help you meet like-minded people.",
            "Feeling homesick is normal, especially when you're in a new environment. One way to ease the transition is to create a comforting space in your new place. Bringing a few familiar items from home can provide a sense of comfort. Additionally, make an effort to attend social events or gatherings to meet new people.",
            "To overcome homesickness, it can be helpful to establish a routine in your new surroundings. Having a schedule can provide a sense of structure and familiarity. When it comes to social adjustment, don't be afraid to initiate conversations and introduce yourself to others. Most people are open to making new friends.",
        ],
        "assignment": [
            "It's essential to prioritize your assignments. Identify the most urgent or important ones and create a task list. Break down each assignment into smaller steps, and tackle them one at a time. This can make the workload more manageable and reduce stress.",
            "Consider setting specific time blocks for working on your assignments. Allocate focused periods for each task, and stick to these time frames. Meeting self-imposed deadlines can help you stay on track and reduce last-minute stress.",
            "Don't hesitate to seek help or support if you're feeling overwhelmed. Reach out to your teachers, professors, or classmates for clarification or assistance. Discussing your challenges with others can provide valuable insights and reduce stress.",
        ],
    },
    "relationship stress": {
        "partner issues": ["Solution P", "Solution Q", "Solution R"],
        "parents issues": ["Solution S", "Solution T", "Solution U"],
        "friends problems": ["Solution V", "Solution W", "Solution X"],
    },
    "parenting stress": {
        "care giver": [
            "I understand that being a caregiver can be very demanding and stressful. Please remember that you are doing a remarkable and compassionate thing. Here are some comforting words and five solutions to help you cope with the stress and anxiety that can come with caregiving:",
            "*Delegate Responsibilities*: Don't hesitate to ask for help and share caregiving duties with others in your support system. It's okay to rely on friends, family, or hired caregivers when needed.",
            "Self-Care: Make time to recharge. It's crucial to ensure you get enough rest, maintain a healthy diet, and engage in activities that bring you joy",
            "*Seek Professional Guidance*: Consider talking to a therapist or counselor to manage the emotional challenges of caregiving. Therapy can provide coping strategies and emotional support",
            "*Set Realistic Expectations*: Understand that it's impossible to be a perfect caregiver. Set realistic expectations for yourself, and acknowledge that it's okay to seek help and take breaks when necessary",
        ],
        "new parent": [
            "It's entirely normal to feel this way as a new parent. You're not alone in these feelings. You're doing an incredible job, even if it doesn't always feel that way. Remember that parenting is a learning journey, and it's okay to make mistakes.",
            " *Take Breaks and Rest*: It's crucial to prioritize self-care. Whenever possible, rest and rejuvenate. A well-rested parent is better equipped to handle the challenges of parenthood.",
            "Seek Support*: Connect with other parents or join a support group. Sharing experiences and advice with those going through similar challenges can be incredibly helpful.",
            " *Communicate with Your Partner*: Open and honest communication with your partner is essential. Work together to share responsibilities and support each other.",
            " *Set Realistic Expectations*: Understand that you can't be a perfect parent. Setting realistic expectations for yourself and your child can help reduce stress and anxiety.",
            "*Professional Help*: If stress and anxiety become overwhelming, consider talking to a therapist or counselor who specializes in parenting and postpartum issues. They can provide valuable guidance and support. Remember it's completely ok to ask for support in tough times",
        ],
        "post partum": [
            "I'm really sorry to hear that you're going through this, but remember, you're not alone, and there is support available. Here are some comforting words and five solutions for dealing with postpartum depression:",
            " *Support Groups*: Join a postpartum depression support group or connect with other mothers who have gone through similar experiences. Sharing your feelings with those who understand can be therapeutic.",
            "*Self-Care*: Prioritize self-care. Even small acts of self-compassion, like getting enough rest, eating well, and engaging in activities you enjoy, can make a significant difference.",
            "*Lean on Your Support System*: Share your feelings with your partner, family, and friends. They can provide emotional support and help with childcare to alleviate some of the stress.",
            "*Medication and Therapy*: Depending on the severity of postpartum depression, a healthcare provider may recommend medication or a combination of medication and therapy. It's essential to discuss treatment options with a healthcare professional.",
            "Remember, it's okay to ask for help, and seeking treatment is a crucial step towards recovery. You are a strong and capable mother, and you can overcome postpartum depression with the right support and care.",
        ],
    },
    "emotional stress": {
        "bereaved": [
            "I'm truly sorry for your loss. Please know that your feelings of grief, anxiety, and sadness are entirely valid, and it's okay to mourn. You are not alone in this. Many people have gone through similar experiences and have found ways to heal. Your loved one will always hold a special place in your heart, and their memory will continue to bring you comfort.",
            "Seek Professional Help: Consider speaking to a therapist or counselor who specializes in grief and loss. They can provide you with valuable guidance and support to help you work through your feelings.",
            "Join a Support Group: Connecting with others who have experienced a similar loss can be incredibly therapeutic. Consider joining a bereavement support group to share your feelings and experiences.",
            "Self-Care: Prioritize self-care and your emotional well-being. This can include activities like meditation, yoga, or engaging in hobbies that bring you joy. Taking care of your physical health by eating well and getting enough rest is equally important.",
            "Remember that healing from the loss of a loved one is a journey, and it's normal to have both good and bad days. Be patient with yourself, and don't hesitate to seek help and support when needed. You are not alone, and there are people who care about your well-being.",
        ],
        "trust issues": [
            "It's completely normal to have trust issues, and your feelings are valid. Many people go through similar challenges, and you're not alone in this. Healing takes time, and it's okay to take the necessary time to rebuild trust, both in yourself and in others.",
            "Therapy or Counseling: Consider talking to a therapist or counselor who specializes in trust and relationship issues. They can help you explore the root causes of your trust issues and provide strategies for building and maintaining trust in your relationships.",
            "Self-Reflection: Take some time for self-reflection to understand the origins of your trust issues. Journaling or discussing your thoughts and feelings with a trusted friend can help you gain insight into the underlying causes of your anxiety.",
            "Mindfulness and Relaxation Techniques: Practices like mindfulness meditation, deep breathing, and progressive muscle relaxation can help reduce anxiety and increase your ability to manage stress. Incorporating these techniques into your daily routine can provide a sense of calm and control.",
            "Remember that healing from trust issues is a process that may take time, but with the right support and strategies, you can overcome anxiety and build healthier, more trusting relationships. Don't hesitate to seek help from professionals or trusted individuals in your life who can support you on this journey.",
        ],
        "intimacy problems": [
            "Your feelings of anxiety in your intimate relationship are valid, and it's okay to acknowledge and address them.",
            "Open Communication: Honest and open communication with your partner is key. Share your feelings and concerns, and encourage your partner to do the same. A safe and understanding environment for discussion can lead to mutual understanding and solutions.",
            "Couples Therapy: Consider seeking couples therapy or counseling with a qualified therapist who specializes in relationship and intimacy issues. Professional guidance can help you both address the root causes of intimacy problems and work on solutions together.",
            "Self-Exploration: Spend time exploring your own needs and desires in the context of intimacy. Self-reflection and self-awareness can help you better communicate your needs to your partner and increase your confidence in the relationship.",
            "Intimacy Exercises: Engage in exercises or activities designed to promote intimacy and connection, such as cuddling, shared hobbies, or trying new experiences together. Building emotional and physical closeness gradually can help ease anxiety and improve your connection.",
            "Remember that addressing intimacy issues in a relationship is a process that may take time and effort from both partners. With open communication, support, and a willingness to work on the relationship, it's possible to improve intimacy and build a stronger and more fulfilling connection with your partner.",
        ],
        "recovery": ["Your decision to pursue recovery is a courageous and positive step toward a healthier and more fulfilling life. You are not alone on this path. Many people have successfully overcome substance abuse and unhealthy practices, and you can too.",
            "Professional Guidance: Consider working with a qualified addiction counselor or therapist who specializes in substance abuse and recovery. They can provide you with the tools and strategies to manage anxiety and develop a strong foundation for sobriety.",
            "Joining a support group or 12-step program can provide you with a network of individuals who understand your struggles. Sharing your experiences with others who have similar journeys can offer encouragement and motivation.",
            "Self-Care: Prioritize self-care as a way to manage anxiety. This includes maintaining a healthy lifestyle through proper nutrition, regular exercise, and sufficient rest. Engaging in stress-reduction techniques such as mindfulness meditation can also be beneficial.",
            "Recovery is a process that requires time and patience. It's important to celebrate your successes, no matter how small they may seem, and to be gentle with yourself during moments of anxiety or doubt. You have the strength to overcome these challenges and build a healthier, happier life. Seeking help, maintaining self-care, and staying connected to a supportive community will be key in your recovery journey.",
        ],
        "trauma": ["Solution Y", "Solution Z", "Solution AA"],
        "general": ["Solution Y", "Solution Z", "Solution AA"],
        "drug stress": ["Solution Y", "Solution Z", "Solution AA"],
        "health": ["Solution Y", "Solution Z", "Solution AA"],
        "loved health": ["Solution Y", "Solution Z", "Solution AA"],
    },
}

# Function to retrieve solutions based on user input
def get_solutions(user_domain, user_input):
    user_domain = user_domain.lower()
    problems = user_input.lower()

    # Check if any keywords match the user input
    for keyword, problems in keyword_to_problem.items():
        if keyword in user_input:
            user_problem = problems
            break
    else:
        user_problem = None

    # Get solutions based on the user's problem
    solutions = structured_data.get(user_domain, {}).get(user_problem, [])

    return user_problem, solutions

@app.route('/', methods=['GET', 'POST'])
def index():
    user_problem = ""
    solutions = []

    if request.method == 'POST':
        user_domain = request.form['user_domain']
        user_input = request.form['problems']

        user_problem, solutions = get_solutions(user_domain,user_input)

    return render_template('index.html', user_problem=user_problem, solutions=solutions)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(debug=True)
    app.run(debug=True)
    app.run(debug=True)