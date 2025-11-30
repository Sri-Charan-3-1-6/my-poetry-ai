# Fix the creatures HTML in app.py

def render_flying_creatures():
    """Add animated birds and butterflies floating across the screen"""
    creatures_html = """
    <div class="flying-creatures">
        <!-- Flying Birds -->
        <div class="flying-bird bird1">🕊️</div>
        <div class="flying-bird bird2">🐦</div>
        <div class="flying-bird bird3">🦅</div>
        <div class="flying-bird bird4">🦜</div>
        <div class="flying-bird bird5">🐧</div>
        <div class="flying-bird bird6">🦆</div>
        
        <!-- Floating Butterflies -->
        <div class="floating-butterfly butterfly1">🦋</div>
        <div class="floating-butterfly butterfly2">🦋</div>
        <div class="floating-butterfly butterfly3">🦋</div>
        <div class="floating-butterfly butterfly4">🦋</div>
        
        <!-- Additional Nature Elements -->
        <div class="floating-leaf leaf1">🍃</div>
        <div class="floating-leaf leaf2">🍂</div>
        <div class="floating-petal petal1">🌸</div>
        
        <!-- Test element with simple animation -->
        <div style="position: absolute; top: 50px; font-size: 30px; color: red; animation: randomFly1 3s linear infinite;">🔴</div>
    </div>
    

    """
    st.markdown(creatures_html, unsafe_allow_html=True)

print("Copy the function above and replace the existing one in app.py")