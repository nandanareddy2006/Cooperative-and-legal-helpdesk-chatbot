import streamlit as st
from backend.main import process_query

st.set_page_config(
    page_title="Sahakaar Saathi",
    page_icon="🤝",
    layout="centered"
)

st.title("🤝 Sahakaar Saathi")
st.subheader("Cooperative & Legal Helpdesk")

st.write(
    "Ask questions about cooperative societies, "
    "legal rights, procedures and grievances."
)

question = st.text_area(
    "Describe your issue",
    placeholder="Example: How do I file a dispute under Section 61?"
)

language = st.selectbox(
    "Language",
    ["English"]
)

if st.button("Ask Sahakaar Saathi", type="primary"):

    if not question.strip():
        st.warning("Please enter your question.")

    else:
        with st.spinner("Processing..."):

            try:
                result = process_query(
                    query_text=question,
                    jurisdiction="Telangana",
                    language=language
                )

                st.success("Response generated")

                st.markdown("### Answer")
                st.write(result["answer"])

                st.markdown("### Category")
                st.write(result["category"])

                if result.get("procedure"):
                    st.markdown("### Procedure")
                    st.json(result["procedure"])

                if result.get("grievance_suggestion"):
                    st.markdown("### Grievance Information")
                    st.json(result["grievance_suggestion"])

                if result.get("suggested_followups"):
                    st.markdown("### Suggested Questions")

                    for item in result["suggested_followups"]:
                        st.write("• " + item)

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)
