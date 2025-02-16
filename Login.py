import streamlit as st

def main():
    ## TODO: Work on the design
    
    st.set_page_config(page_title="Patient Login", page_icon="🏥")
    
    st.title("Patient Login/Signup")
    
    full_name = st.text_input("Full Name")
    email = st.text_input("Email", type="default")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        if full_name and email and password:
            st.success(f"Welcome, {full_name}! Redirecting to Patient Dashboard...")
            # st.experimental_rerun()
            # nav_page("Dashboard")
        else:
            st.error("Please fill in all fields.")
    
    st.markdown("Don't have an account? [Sign Up](#)")
    st.markdown('</div>', unsafe_allow_html=True)
    
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

if __name__ == "__main__":
    main()
