import streamlit as st
import os
import json
import base64
from ai_helpers import (
    enhance_course_description, 
    process_document, 
    generate_learning_objectives,
    generate_prerequisites,
    generate_learning_methods,
    generate_course_structure,
    generate_chapter_content,
    generate_quiz,
    generate_podcast_script,
    generate_podcast_audio
)

# Configuration de la page
st.set_page_config(
    page_title="ZEY LMS - Assistant de Création de Contenu Pédagogique",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des variables de session si elles n'existent pas
if 'api_provider' not in st.session_state:
    st.session_state.api_provider = "openai"
if 'enhanced_description' not in st.session_state:
    st.session_state.enhanced_description = ""
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []
if 'document_embeddings' not in st.session_state:
    st.session_state.document_embeddings = {}
if 'learning_methods' not in st.session_state:
    st.session_state.learning_methods = []
if 'learning_objectives' not in st.session_state:
    st.session_state.learning_objectives = []
if 'prerequisites' not in st.session_state:
    st.session_state.prerequisites = []
if 'course_structure' not in st.session_state:
    st.session_state.course_structure = {"modules": []}
if 'chapter_contents' not in st.session_state:
    st.session_state.chapter_contents = {}
if 'quizzes' not in st.session_state:
    st.session_state.quizzes = {}
if 'podcast_script' not in st.session_state:
    st.session_state.podcast_script = {}
if 'podcast_audio' not in st.session_state:
    st.session_state.podcast_audio = {}

# Titre principal de l'application
st.title("ZEY LMS - Assistant de Création de Contenu Pédagogique")

# Création des onglets
tabs = st.tabs(["Infos cours", "Prérequis", "Générer un cours", "Générer un quizz", "Générer un podcast"])

# Fonction pour améliorer la description
def enhance_description():
    title = st.session_state.course_title
    initial_description = st.session_state.course_description
    
    if not title or not initial_description:
        st.session_state.enhanced_description = "Veuillez fournir un titre et une description initiale."
        return
    
    with st.spinner("Amélioration de la description en cours..."):
        enhanced = enhance_course_description(
            title=title,
            initial_description=initial_description,
            api_provider=st.session_state.api_provider
        )
        st.session_state.enhanced_description = enhanced
        st.session_state.course_description = enhanced

# Fonction pour générer des objectifs d'apprentissage
def generate_objectives():
    title = st.session_state.course_title
    description = st.session_state.course_description
    
    if not title or not description:
        st.warning("Veuillez d'abord remplir le titre et la description du cours dans l'onglet 'Infos cours'.")
        return
    
    with st.spinner("Génération des objectifs d'apprentissage en cours..."):
        objectives = generate_learning_objectives(title, description)
        st.session_state.learning_objectives = objectives

# Fonction pour générer des prérequis
def generate_prereqs():
    title = st.session_state.course_title
    description = st.session_state.course_description
    
    if not title or not description:
        st.warning("Veuillez d'abord remplir le titre et la description du cours dans l'onglet 'Infos cours'.")
        return
    
    with st.spinner("Génération des prérequis en cours..."):
        prereqs = generate_prerequisites(title, description)
        st.session_state.prerequisites = prereqs

# Fonction pour générer des méthodes d'apprentissage
def generate_methods():
    title = st.session_state.course_title
    description = st.session_state.course_description
    
    if not title or not description:
        st.warning("Veuillez d'abord remplir le titre et la description du cours dans l'onglet 'Infos cours'.")
        return
    
    with st.spinner("Génération des méthodes d'apprentissage en cours..."):
        methods = generate_learning_methods(title, description)
        st.session_state.learning_methods = methods

# Fonction pour générer la structure du cours
def generate_course_content():
    title = st.session_state.course_title
    description = st.session_state.course_description
    duration = st.session_state.get("duration", "")
    difficulty = st.session_state.get("difficulty", "Beginner")
    
    try:
        num_modules = int(st.session_state.get("modules", "1"))
    except ValueError:
        num_modules = 1
    
    if not title or not description:
        st.warning("Veuillez d'abord remplir le titre et la description du cours dans l'onglet 'Infos cours'.")
        return
    
    # Récupérer le texte des documents uploadés si disponible
    document_text = ""
    document_embeddings = []
    if st.session_state.uploaded_documents:
        # Concaténer le texte de tous les documents
        document_text = "\n\n".join([doc["text"] for doc in st.session_state.uploaded_documents])
        # Utiliser les embeddings du premier document (si disponible)
        if st.session_state.document_embeddings:
            document_embeddings = list(st.session_state.document_embeddings.values())[0]
    
    with st.spinner("Génération de la structure du cours en cours..."):
        course_structure = generate_course_structure(
            course_title=title,
            course_description=description,
            duration=duration,
            difficulty=difficulty,
            num_modules=num_modules,
            document_text=document_text,
            document_embeddings=document_embeddings
        )
        
        st.session_state.course_structure = course_structure

# Fonction pour générer le contenu détaillé d'un chapitre
def generate_chapter_detail(module_number, chapter_number):
    title = st.session_state.course_title
    description = st.session_state.course_description
    
    # Trouver le module et le chapitre correspondants
    module = None
    chapter = None
    
    for mod in st.session_state.course_structure["modules"]:
        if mod["module_number"] == module_number:
            module = mod
            for chap in mod["chapters"]:
                if chap["chapter_number"] == chapter_number:
                    chapter = chap
                    break
            break
    
    if not module or not chapter:
        st.error(f"Module {module_number} ou chapitre {chapter_number} non trouvé.")
        return
    
    # Clé unique pour ce chapitre
    chapter_key = f"{module_number}_{chapter_number}"
    
    # Vérifier si le contenu du chapitre a déjà été généré
    if chapter_key in st.session_state.chapter_contents:
        return
    
    # Récupérer le texte des documents uploadés si disponible
    document_text = ""
    document_embeddings = []
    if st.session_state.uploaded_documents:
        # Concaténer le texte de tous les documents
        document_text = "\n\n".join([doc["text"] for doc in st.session_state.uploaded_documents])
        # Utiliser les embeddings du premier document (si disponible)
        if st.session_state.document_embeddings:
            document_embeddings = list(st.session_state.document_embeddings.values())[0]
    
    with st.spinner(f"Génération du contenu détaillé pour le chapitre {chapter_number}..."):
        chapter_content = generate_chapter_content(
            course_title=title,
            course_description=description,
            module_title=module["module_title"],
            chapter_title=chapter["chapter_title"],
            chapter_description=chapter["description"],
            key_points=chapter["key_points"],
            document_text=document_text,
            document_embeddings=document_embeddings
        )
        
        # Stocker le contenu du chapitre
        st.session_state.chapter_contents[chapter_key] = chapter_content

# Fonction pour ajouter une méthode d'apprentissage
def add_learning_method(method=""):
    st.session_state.learning_methods.append(method)

# Fonction pour supprimer une méthode d'apprentissage
def remove_learning_method(index):
    if len(st.session_state.learning_methods) > 0:
        st.session_state.learning_methods.pop(index)

# Fonction pour mettre à jour une méthode d'apprentissage
def update_learning_method(index, method):
    st.session_state.learning_methods[index] = method

# Fonction pour ajouter un objectif d'apprentissage
def add_learning_objective(objective):
    st.session_state.learning_objectives.append(objective)

# Fonction pour supprimer un objectif d'apprentissage
def remove_learning_objective(index):
    st.session_state.learning_objectives.pop(index)

# Fonction pour ajouter un prérequis
def add_prerequisite(prerequisite):
    st.session_state.prerequisites.append(prerequisite)

# Fonction pour supprimer un prérequis
def remove_prerequisite(index):
    st.session_state.prerequisites.pop(index)

# Fonction pour traiter les documents uploadés
def process_uploaded_documents(uploaded_files):
    if not uploaded_files:
        return
    
    # Vérifier si la clé API OpenAI est disponible
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("Clé API OpenAI non trouvée. Veuillez configurer la clé API dans la barre latérale.")
        return
    
    for uploaded_file in uploaded_files:
        # Vérifier si le fichier a déjà été traité
        if uploaded_file.name in [doc["name"] for doc in st.session_state.uploaded_documents]:
            continue
        
        # Vérifier l'extension du fichier
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in ['.pdf', '.docx', '.pptx', '.txt']:
            st.warning(f"Type de fichier non pris en charge: {file_extension}. Seuls les fichiers PDF, DOCX, PPTX et TXT sont acceptés.")
            continue
        
        # Vérifier la taille du fichier (max 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB en octets
            st.warning(f"Le fichier {uploaded_file.name} dépasse la taille maximale de 10MB.")
            continue
        
        with st.spinner(f"Traitement du document: {uploaded_file.name}..."):
            try:
                # Traiter le document et créer des embeddings
                text, embeddings = process_document(uploaded_file, uploaded_file.name, api_key)
                
                # Stocker les informations du document
                document_info = {
                    "name": uploaded_file.name,
                    "type": file_extension,
                    "size": uploaded_file.size,
                    "text": text[:1000] + "..." if len(text) > 1000 else text  # Aperçu du texte
                }
                
                # Ajouter le document à la liste des documents uploadés
                st.session_state.uploaded_documents.append(document_info)
                
                # Stocker les embeddings
                st.session_state.document_embeddings[uploaded_file.name] = embeddings
                
                st.success(f"Document traité avec succès: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Erreur lors du traitement du document {uploaded_file.name}: {str(e)}")

# Fonction pour générer un quiz
def generate_module_quiz(module_number, num_questions, difficulty_level, question_types):
    title = st.session_state.course_title
    
    # Vérifier si la structure du cours a été générée
    if not st.session_state.course_structure or "modules" not in st.session_state.course_structure:
        st.error("Veuillez d'abord générer la structure du cours dans l'onglet 'Générer un cours'.")
        return
    
    # Trouver le module correspondant
    module = None
    for mod in st.session_state.course_structure["modules"]:
        if mod["module_number"] == module_number:
            module = mod
            break
    
    if not module:
        st.error(f"Module {module_number} non trouvé.")
        return
    
    # Clé unique pour ce quiz
    quiz_key = f"module_{module_number}_quiz"
    
    # Vérifier si le quiz a déjà été généré
    if quiz_key in st.session_state.quizzes:
        return
    
    with st.spinner(f"Génération du quiz pour le module {module_number}..."):
        quiz = generate_quiz(
            course_title=title,
            module_data=module,
            num_questions=num_questions,
            difficulty_level=difficulty_level,
            question_types=question_types
        )
        
        # Stocker le quiz
        st.session_state.quizzes[quiz_key] = quiz

# Fonction pour générer un script de podcast
def generate_podcast_script_content():
    title = st.session_state.course_title
    description = st.session_state.course_description
    
    # Vérifier si la structure du cours a été générée
    if not st.session_state.course_structure or "modules" not in st.session_state.course_structure:
        st.error("Veuillez d'abord générer la structure du cours dans l'onglet 'Générer un cours'.")
        return
    
    # Récupérer les paramètres du podcast
    podcast_format = st.session_state.get("podcast_format", "Interview")
    podcast_duration = st.session_state.get("podcast_duration", "15-20 minutes")
    target_audience = st.session_state.get("podcast_audience", "Étudiants")
    
    with st.spinner("Génération du script de podcast en cours..."):
        podcast_script = generate_podcast_script(
            course_title=title,
            course_description=description,
            course_structure=st.session_state.course_structure,
            podcast_format=podcast_format,
            podcast_duration=podcast_duration,
            target_audience=target_audience
        )
        
        # Stocker le script
        st.session_state.podcast_script = podcast_script

# Fonction pour générer l'audio du podcast
def generate_podcast_audio_content(script_text, voice):
    with st.spinner("Génération de l'audio du podcast en cours..."):
        audio_result = generate_podcast_audio(
            script_text=script_text,
            voice=voice
        )
        
        # Stocker l'audio
        st.session_state.podcast_audio = audio_result

# Onglet 1: Infos cours
with tabs[0]:
    st.header("Create New Course")
    
    # API Provider selection in sidebar
    with st.sidebar:
        st.subheader("AI Settings")
        st.session_state.api_provider = st.radio(
            "Select AI Provider",
            options=["openai", "anthropic"],
            index=0 if st.session_state.api_provider == "openai" else 1
        )
        
        # API Key inputs
        if st.session_state.api_provider == "openai":
            openai_api_key = st.text_input("OpenAI API Key", type="password", 
                                          value=os.environ.get("OPENAI_API_KEY", ""), 
                                          key="openai_key")
            if openai_api_key:
                os.environ["OPENAI_API_KEY"] = openai_api_key
        else:
            anthropic_api_key = st.text_input("Anthropic API Key", type="password", 
                                             value=os.environ.get("ANTHROPIC_API_KEY", ""), 
                                             key="anthropic_key")
            if anthropic_api_key:
                os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
    
    # Course Title
    st.subheader("Course Title")
    titre_cours = st.text_input("", placeholder="Enter course title", label_visibility="collapsed", key="course_title")
    
    # Course Description
    st.subheader("Course Description")
    col1, col2 = st.columns([5, 1])
    with col1:
        description = st.text_area("", placeholder="Enter course description", height=120, label_visibility="collapsed", key="course_description")
    with col2:
        st.write("")
        st.write("")
        ai_button = st.button("🔍", help="AI assistance for description", key="ai_description", on_click=enhance_description)
    
    # Display enhanced description if available
    if st.session_state.enhanced_description and ai_button:
        st.info("Description améliorée par l'IA:")
        st.write(st.session_state.enhanced_description)
    
    # Category and Duration in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Category")
        category = st.selectbox("", ["Select a category", "Programming", "Data Science", "Business", "Design", "Marketing", "Language"], label_visibility="collapsed", key="category")
    with col2:
        st.subheader("Duration")
        duration = st.text_input("", placeholder="e.g., 8 weeks", label_visibility="collapsed", key="duration")
    
    # Difficulty Level and Number of Modules in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Difficulty Level")
        difficulty = st.selectbox("", ["Beginner", "Intermediate", "Advanced", "Expert"], label_visibility="collapsed", key="difficulty")
    with col2:
        st.subheader("Number of Modules")
        modules = st.text_input("", placeholder="1", label_visibility="collapsed", key="modules")
    
    # Price
    st.subheader("Price ($)")
    price = st.text_input("", placeholder="0", label_visibility="collapsed", key="price")
    
    # Course Image
    st.subheader("Course Image")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/150x150?text=+", width=150)
    with col2:
        st.button("🔍 Create with AI", use_container_width=True, key="create_image_ai")
        st.caption("Upload a course image (recommended size: 600×400)")
    
    # Course Documents
    st.subheader("Course Documents")
    
    # Uploader de documents
    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=["pdf", "docx", "pptx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: PDF, Word, PowerPoint, Text (max 10MB)"
    )
    
    # Traiter les documents uploadés
    if uploaded_files:
        if st.button("Process Documents", key="process_docs"):
            process_uploaded_documents(uploaded_files)
    
    # Afficher les documents uploadés
    if st.session_state.uploaded_documents:
        st.subheader("Documents de référence")
        for doc in st.session_state.uploaded_documents:
            st.write(f"- {doc['name']}")
    
    st.caption("Supported formats: PDF, Word, PowerPoint, Text (max 10MB)")
    
    # Create Course and Save as Draft buttons
    col1, col2 = st.columns([1, 3])
    with col1:
        st.button("Create Course", type="primary", key="create_course")
    with col2:
        st.button("Save as Draft", key="save_draft")

# Onglet 2: Prérequis
with tabs[1]:
    st.header("Course Setup")
    
    # Section 1: Learning Objectives
    st.subheader("Learning Objectives")
    st.write("What will students learn in this course?")
    
    # Bouton pour générer des objectifs d'apprentissage avec l'IA
    col1, col2 = st.columns([5, 1])
    with col2:
        generate_obj_button = st.button("Generate with AI", key="generate_objectives", on_click=generate_objectives)
    
    # Afficher les objectifs d'apprentissage existants
    for i, objective in enumerate(st.session_state.learning_objectives):
        col1, col2 = st.columns([20, 1])
        with col1:
            st.text_input(f"Objective {i+1}", value=objective, key=f"objective_{i}")
        with col2:
            if st.button("🗑️", key=f"delete_objective_{i}"):
                remove_learning_objective(i)
                st.rerun()
    
    # Ajouter un nouvel objectif manuellement
    new_objective = st.text_input("Add a new learning objective", key="new_objective")
    if st.button("Add Objective", key="add_objective") and new_objective:
        add_learning_objective(new_objective)
        st.session_state.new_objective = ""  # Clear the input
        st.rerun()
    
    # Section 2: Prerequisites
    st.markdown("---")
    st.subheader("Prerequisites")
    st.write("What should students know before taking this course?")
    
    # Bouton pour générer des prérequis avec l'IA
    col1, col2 = st.columns([5, 1])
    with col2:
        generate_prereq_button = st.button("Generate with AI", key="generate_prerequisites", on_click=generate_prereqs)
    
    # Afficher les prérequis existants
    for i, prerequisite in enumerate(st.session_state.prerequisites):
        col1, col2 = st.columns([20, 1])
        with col1:
            st.text_input(f"Prerequisite {i+1}", value=prerequisite, key=f"prerequisite_{i}")
        with col2:
            if st.button("🗑️", key=f"delete_prerequisite_{i}"):
                remove_prerequisite(i)
                st.rerun()
    
    # Ajouter un nouveau prérequis manuellement
    new_prerequisite = st.text_input("Add a new prerequisite", key="new_prerequisite")
    if st.button("Add Prerequisite", key="add_prerequisite") and new_prerequisite:
        add_prerequisite(new_prerequisite)
        st.session_state.new_prerequisite = ""  # Clear the input
        st.rerun()
    
    # Section 3: Learning Methods
    st.markdown("---")
    st.subheader("Learning Methods")
    st.write("How will you deliver the course content?")
    
    # Bouton pour générer des méthodes d'apprentissage avec l'IA
    col1, col2 = st.columns([5, 1])
    with col2:
        generate_methods_button = st.button("Generate with AI", key="generate_methods", on_click=generate_methods)
    
    # Afficher les méthodes d'apprentissage existantes
    for i, method in enumerate(st.session_state.learning_methods):
        col1, col2 = st.columns([20, 1])
        with col1:
            method_value = st.text_input(f"Method {i+1}", value=method, key=f"method_{i}")
            # Mettre à jour la méthode si elle a changé
            if method_value != method:
                update_learning_method(i, method_value)
        with col2:
            if st.button("🗑️", key=f"delete_method_{i}"):
                remove_learning_method(i)
                st.rerun()
    
    # Ajouter une nouvelle méthode manuellement
    new_method = st.text_input("Add a new learning method", key="new_method")
    if st.button("Add Method", key="add_method") and new_method:
        add_learning_method(new_method)
        st.session_state.new_method = ""  # Clear the input
        st.rerun()
    
    # Boutons de navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("← Back to Courses", key="back_to_courses")
    with col2:
        col3, col4 = st.columns([1, 1])
        with col3:
            st.button("Skip Setup", key="skip_setup")
        with col4:
            st.button("Save and Continue →", type="primary", key="save_continue")

# Onglet 3: Générer un cours
with tabs[2]:
    st.header("Générateur de contenu de cours")
    st.write("Utilisez l'IA pour générer du contenu pédagogique pour votre cours.")
    
    # Vérifier si les informations de base du cours sont disponibles
    if not st.session_state.get("course_title") or not st.session_state.get("course_description"):
        st.warning("Veuillez d'abord remplir le titre et la description du cours dans l'onglet 'Infos cours'.")
    else:
        # Afficher les informations du cours
        st.subheader("Informations du cours")
        st.write(f"**Titre:** {st.session_state.course_title}")
        st.write(f"**Description:** {st.session_state.course_description}")
        
        if st.session_state.get("duration"):
            st.write(f"**Durée:** {st.session_state.duration}")
        
        if st.session_state.get("difficulty"):
            st.write(f"**Niveau de difficulté:** {st.session_state.difficulty}")
        
        # Nombre de modules
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Nombre de modules:** {st.session_state.get('modules', '1')}")
        with col2:
            generate_button = st.button("Générer la structure du cours", key="generate_course_structure", on_click=generate_course_content)
        
        # Afficher les documents uploadés
        if st.session_state.uploaded_documents:
            st.subheader("Documents de référence")
            for doc in st.session_state.uploaded_documents:
                st.write(f"- {doc['name']}")
        
        # Afficher la structure du cours si elle a été générée
        if "modules" in st.session_state.course_structure and st.session_state.course_structure["modules"]:
            st.subheader("Structure du cours")
            
            # Créer des onglets pour chaque module
            module_tabs = st.tabs([f"Module {module['module_number']}: {module['module_title']}" 
                                 for module in st.session_state.course_structure["modules"]])
            
            # Remplir chaque onglet de module avec ses chapitres
            for i, module_tab in enumerate(module_tabs):
                with module_tab:
                    module = st.session_state.course_structure["modules"][i]
                    
                    # Afficher les chapitres du module
                    for chapter in module["chapters"]:
                        with st.expander(f"Chapitre {chapter['chapter_number']}: {chapter['chapter_title']}"):
                            st.write(f"**Description:** {chapter['description']}")
                            
                            st.write("**Points clés:**")
                            for point in chapter['key_points']:
                                st.write(f"- {point}")
                            
                            # Clé unique pour ce chapitre
                            chapter_key = f"{module['module_number']}_{chapter['chapter_number']}"
                            
                            # Vérifier si le contenu détaillé du chapitre a déjà été généré
                            if chapter_key in st.session_state.chapter_contents:
                                # Afficher le contenu détaillé du chapitre
                                chapter_content = st.session_state.chapter_contents[chapter_key]
                                
                                # Vérifier s'il y a une erreur
                                if "error" in chapter_content:
                                    st.error(f"Erreur: {chapter_content['error']}")
                                else:
                                    # Afficher l'introduction
                                    st.markdown("### Introduction")
                                    st.write(chapter_content["introduction"])
                                    
                                    # Afficher les sections
                                    for section in chapter_content["sections"]:
                                        st.markdown(f"### {section['title']}")
                                        st.write(section["content"])
                                        
                                        # Afficher les exemples
                                        if "examples" in section and section["examples"]:
                                            st.markdown("**Exemples:**")
                                            for example in section["examples"]:
                                                st.markdown(f"- *{example}*")
                                    
                                    # Afficher la conclusion
                                    st.markdown("### Conclusion")
                                    st.write(chapter_content["conclusion"])
                                    
                                    # Afficher les exercices
                                    if "exercises" in chapter_content and chapter_content["exercises"]:
                                        st.markdown("### Exercices")
                                        for j, exercise in enumerate(chapter_content["exercises"]):
                                            st.markdown(f"**Exercice {j+1}:** {exercise['question']}")
                                            st.markdown(f"*Réponse/Indice:* {exercise['answer']}")
                                            st.markdown("---")
                            else:
                                # Bouton pour générer le contenu détaillé du chapitre
                                if st.button(f"Générer contenu détaillé", key=f"generate_chapter_{module['module_number']}_{chapter['chapter_number']}"):
                                    generate_chapter_detail(module['module_number'], chapter['chapter_number'])
                                    st.rerun()
            
            # Bouton pour exporter la structure du cours
            st.download_button(
                label="Exporter la structure du cours (JSON)",
                data=json.dumps(st.session_state.course_structure, indent=2, ensure_ascii=False),
                file_name="structure_cours.json",
                mime="application/json"
            )
        
        elif generate_button:
            st.info("La structure du cours est en cours de génération...")
        else:
            st.info("Cliquez sur 'Générer la structure du cours' pour créer une structure hiérarchique de modules et chapitres.")

# Onglet 4: Générer un quizz
with tabs[3]:
    st.header("Générateur de quizz")
    st.write("Créez des quizz interactifs pour évaluer les connaissances.")
    
    # Vérifier si la structure du cours a été générée
    if not st.session_state.course_structure or "modules" not in st.session_state.course_structure or not st.session_state.course_structure["modules"]:
        st.warning("Veuillez d'abord générer la structure du cours dans l'onglet 'Générer un cours'.")
    else:
        # Sélection du module
        module_options = [f"Module {module['module_number']}: {module['module_title']}" for module in st.session_state.course_structure["modules"]]
        selected_module = st.selectbox("Sélectionnez un module", module_options)
        
        # Extraire le numéro du module sélectionné
        selected_module_number = int(selected_module.split(":")[0].replace("Module ", "").strip())
        
        col1, col2 = st.columns(2)
        with col1:
            # Nombre de questions
            nb_questions = st.number_input("Nombre de questions", min_value=1, max_value=50, value=10)
            
            # Niveau de difficulté
            difficulte = st.select_slider("Niveau de difficulté", 
                                         options=["Très facile", "Facile", "Moyen", "Difficile", "Très difficile"], 
                                         value="Moyen")
        
        with col2:
            # Types de questions
            type_questions = st.multiselect("Types de questions", 
                                           ["Choix multiple", "Vrai/Faux", "Questions directes"], 
                                           default=["Choix multiple", "Vrai/Faux"])
            
            # Temps limite (fonctionnalité future)
            temps_limite = st.checkbox("Imposer un temps limite", value=False)
        
        # Bouton pour générer le quiz
        if st.button("Générer le quizz", type="primary"):
            # Vérifier si les types de questions sont sélectionnés
            if not type_questions:
                st.error("Veuillez sélectionner au moins un type de question.")
            else:
                # Générer le quiz
                generate_module_quiz(selected_module_number, nb_questions, difficulte, type_questions)
        
        # Clé unique pour ce quiz
        quiz_key = f"module_{selected_module_number}_quiz"
        
        # Afficher le quiz s'il a été généré
        if quiz_key in st.session_state.quizzes:
            quiz = st.session_state.quizzes[quiz_key]
            
            # Vérifier s'il y a une erreur
            if "error" in quiz:
                st.error(f"Erreur: {quiz['error']}")
            else:
                st.success(f"Quiz généré avec succès pour le module {selected_module_number}: {quiz['module_title']}")
                
                # Afficher les questions du quiz
                st.subheader(f"Quiz: {quiz['quiz_title']}")
                st.write(f"Niveau de difficulté: {quiz['difficulty_level']}")
                
                # Créer un accordéon pour chaque question
                for question in quiz["questions"]:
                    with st.expander(f"Question {question['question_number']}: {question['question_text']}"):
                        st.write(f"**Type de question:** {question['question_type']}")
                        
                        # Afficher les options pour les questions à choix multiple
                        if question['question_type'] == "Choix multiple" and "options" in question:
                            st.write("**Options:**")
                            for i, option in enumerate(question["options"]):
                                st.write(f"{chr(65+i)}. {option}")
                        
                        # Afficher la réponse correcte
                        st.write(f"**Réponse correcte:** {question['correct_answer']}")
                        
                        # Afficher l'explication
                        st.write(f"**Explication:** {question['explanation']}")
                
                # Bouton pour exporter le quiz
                st.download_button(
                    label="Exporter le quiz (JSON)",
                    data=json.dumps(quiz, indent=2, ensure_ascii=False),
                    file_name=f"quiz_module_{selected_module_number}.json",
                    mime="application/json"
                )

# Onglet 5: Générer un podcast
with tabs[4]:
    st.header("Générateur de podcast éducatif")
    st.write("Transformez votre contenu en format audio pour un apprentissage flexible.")
    
    # Vérifier si la structure du cours a été générée
    if not st.session_state.course_structure or "modules" not in st.session_state.course_structure or not st.session_state.course_structure["modules"]:
        st.warning("Veuillez d'abord générer la structure du cours dans l'onglet 'Générer un cours'.")
    else:
        # Afficher les informations du cours
        st.subheader("Informations du cours")
        st.write(f"**Titre:** {st.session_state.course_title}")
        st.write(f"**Description:** {st.session_state.course_description}")
        
        # Paramètres du podcast
        st.subheader("Paramètres du podcast")
        
        col1, col2 = st.columns(2)
        with col1:
            # Format du podcast
            podcast_format = st.selectbox("Format du podcast", 
                                         ["Interview", "Monologue", "Discussion", "Débat"], 
                                         key="podcast_format")
            
            # Durée du podcast
            podcast_duration_options = ["5-10 minutes", "10-15 minutes", "15-20 minutes", "20-30 minutes", "30+ minutes"]
            podcast_duration = st.selectbox("Durée cible", podcast_duration_options, index=2, key="podcast_duration")
        
        with col2:
            # Public cible
            podcast_audience = st.selectbox("Public cible", 
                                           ["Étudiants", "Professionnels", "Grand public", "Experts du domaine"], 
                                           key="podcast_audience")
            
            # Voix pour la synthèse vocale
            voice_options = {
                "Alloy (neutre)": "alloy",
                "Echo (grave)": "echo",
                "Fable (expressif)": "fable",
                "Onyx (professionnel)": "onyx",
                "Nova (féminin)": "nova",
                "Shimmer (léger)": "shimmer"
            }
            voice_display = st.selectbox("Voix pour la synthèse vocale", list(voice_options.keys()), index=0, key="voice_display")
            voice = voice_options[voice_display]
        
        # Bouton pour générer le script du podcast
        if st.button("Générer le script du podcast", type="primary"):
            generate_podcast_script_content()
        
        # Afficher le script s'il a été généré
        if st.session_state.podcast_script:
            # Vérifier s'il y a une erreur
            if "error" in st.session_state.podcast_script:
                st.error(f"Erreur: {st.session_state.podcast_script['error']}")
            else:
                st.success(f"Script généré avec succès: {st.session_state.podcast_script['podcast_title']}")
                
                # Afficher les informations du podcast
                st.subheader(f"Podcast: {st.session_state.podcast_script['podcast_title']}")
                st.write(f"**Format:** {st.session_state.podcast_script['format']}")
                st.write(f"**Durée estimée:** {st.session_state.podcast_script['duration']}")
                st.write(f"**Public cible:** {st.session_state.podcast_script['target_audience']}")
                
                # Afficher les participants
                if "participants" in st.session_state.podcast_script:
                    st.write("**Participants:**")
                    for participant in st.session_state.podcast_script['participants']:
                        st.write(f"- {participant}")
                
                # Afficher les sections du script
                st.subheader("Script du podcast")
                
                # Créer un texte complet pour la synthèse vocale
                full_script_text = ""
                
                # Afficher chaque section du script
                for section in st.session_state.podcast_script['script_sections']:
                    with st.expander(f"{section['section_title']}"):
                        st.write(section['content'])
                        full_script_text += section['content'] + "\n\n"
                
                # Bouton pour générer l'audio
                if st.button("Générer l'audio du podcast"):
                    generate_podcast_audio_content(full_script_text, voice)
                
                # Afficher l'audio s'il a été généré
                if st.session_state.podcast_audio:
                    # Vérifier s'il y a une erreur
                    if "error" in st.session_state.podcast_audio:
                        st.error(f"Erreur: {st.session_state.podcast_audio['error']}")
                    else:
                        st.subheader("Audio du podcast")
                        
                        # Créer un lecteur audio HTML
                        audio_html = f"""
                        <audio controls>
                            <source src="data:audio/mp3;base64,{st.session_state.podcast_audio['audio_base64']}" type="audio/mp3">
                            Votre navigateur ne supporte pas l'élément audio.
                        </audio>
                        """
                        st.markdown(audio_html, unsafe_allow_html=True)
                        
                        # Bouton pour télécharger l'audio
                        st.download_button(
                            label="Télécharger le podcast (MP3)",
                            data=base64.b64decode(st.session_state.podcast_audio['audio_base64']),
                            file_name=f"{st.session_state.podcast_script['podcast_title'].replace(' ', '_')}.mp3",
                            mime="audio/mp3"
                        )
                
                # Bouton pour exporter le script
                st.download_button(
                    label="Exporter le script (JSON)",
                    data=json.dumps(st.session_state.podcast_script, indent=2, ensure_ascii=False),
                    file_name="script_podcast.json",
                    mime="application/json"
                )
                
                # Bouton pour exporter le script en format texte
                st.download_button(
                    label="Exporter le script (TXT)",
                    data=full_script_text,
                    file_name="script_podcast.txt",
                    mime="text/plain"
                )

# Pied de page
st.markdown("---")
st.markdown("© 2023 ZEY LMS - Tous droits réservés")
