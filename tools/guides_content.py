"""PizarraPad help guides: practical articles for teachers (rendered by build.py under /guides/)."""

LEAD = 'Practical guides for teaching with a board on a projector, TV, tablet or video call.'

GUIDES = [
dict(slug='tablet-stylus-classroom-whiteboard', updated='2026-11-23',
     title='How to Use a Tablet and Stylus as a Classroom Whiteboard',
     short='Tablet and stylus as a classroom whiteboard',
     desc='Turn a Samsung Galaxy Tab with S Pen, an iPad with Apple Pencil or another tablet into a whiteboard on your classroom TV or projector, step by step.',
     body='''<p class="lead">A tablet with a stylus is one of the best whiteboards a classroom can have: you write by hand, face the class, and everyone sees it large on the screen.</p>

<h2>What you need</h2>
<ul><li>A tablet with a stylus: a Samsung Galaxy Tab with S Pen, an iPad with Apple Pencil, a Windows tablet with a pen, or any tablet with a basic stylus.</li>
<li>A way to show the tablet on the big screen: a cable adapter, or a TV or streaming device you can cast to.</li>
<li>A browser. Open <a href="/board/">PizarraPad</a>; there is nothing to install and no account.</li></ul>

<h2>Step 1: Connect the tablet to the screen</h2>
<h3>With a cable (most reliable)</h3>
<ul><li><b>Android tablets with USB-C</b> (most Galaxy Tab S models): use a USB-C to HDMI adapter. Some Samsung tablets open a desktop-style view (Samsung DeX) when connected; you can use PizarraPad there too, or switch to mirroring from the tablet’s quick settings or notification.</li>
<li><b>iPad</b>: use a USB-C or Lightning to HDMI adapter, depending on your iPad.</li></ul>
<h3>Without a cable</h3>
<ul><li><b>Android</b>: use <b>Smart View</b> (Samsung) or <b>Cast</b> to a smart TV or a Chromecast on the same Wi-Fi.</li>
<li><b>iPad</b>: use <b>Screen Mirroring</b> to an Apple TV or an AirPlay-compatible TV.</li></ul>
<p>Wireless is convenient, but it can lag a little behind your pen and depends on the Wi-Fi. For full lessons, a cable is calmer.</p>

<h2>Step 2: Set up the board</h2>
<ol><li>Open PizarraPad and choose a board under <b>⋯</b>: whiteboard, blackboard or greenboard. On most projectors, the blackboard or greenboard is easiest to read.</li>
<li>Pick a background: <b>Lines</b> for handwriting and language lessons, <b>Grid</b> for math and science.</li>
<li>Turn on <b>Pen only</b>. Now only the stylus writes. Your palm can rest on the screen, and fingers scroll and zoom instead of drawing.</li>
<li>Choose <b>⋯ → Full screen</b> so the browser bars disappear from the big screen.</li></ol>
<p>Tip: add PizarraPad to your home screen (in Chrome or Samsung Internet, <i>Add to home screen</i>; on iPad, <i>Share → Add to Home Screen</i>). It then opens like an app, and keeps working when the Wi-Fi drops.</p>

<h2>Step 3: Write so the back row can read</h2>
<ul><li>Use the <b>Thick</b> pen. Pressure works with styluses that support it, so press a little harder for bolder lines.</li>
<li>Write larger than feels natural. Zoom out with two fingers to see the whole page, and zoom in to write details.</li>
<li>Use one or two colors with a purpose: white or yellow for the main content, a second color for examples.</li>
<li>Use the <b>highlighter</b> to mark key words, and the <b>laser</b> to point without leaving marks.</li></ul>

<h2>Step 4: Use pages like a lesson plan</h2>
<p>Add a new page with <b>+</b> for each part of the lesson: warm-up, new idea, worked example, practice. Moving between pages with the arrows is quicker than erasing, and you can go back when a student asks a question.</p>
<p>You can also add a picture with the <b>Image</b> tool, such as a diagram, a map or a photo of a worksheet, and write on top of it. On a tablet, you can take the photo with the camera right there.</p>

<h2>Step 5: After class</h2>
<ul><li>Everything is saved on the tablet automatically.</li>
<li>Use <b>⋯ → Save page as image</b> to share a page with students who were absent, or to keep a record of the lesson.</li>
<li>Use <b>Start a new board</b> for the next class, after saving anything you need.</li></ul>

<h2>Common problems</h2>
<table class="tbl"><thead><tr><th>Problem</th><th>Fix</th></tr></thead><tbody>
<tr><td>My hand leaves marks.</td><td>Turn on <b>Pen only</b>.</td></tr>
<tr><td>The picture on the TV is delayed.</td><td>Use a cable, or move closer to the Wi-Fi router and close other apps.</td></tr>
<tr><td>Notifications pop up on the big screen.</td><td>Turn on Do Not Disturb before the lesson.</td></tr>
<tr><td>The tablet goes to sleep.</td><td>Set the screen timeout to 30 minutes or more, and keep it plugged in.</td></tr></tbody></table>
<p>More setups, including laptops and smart boards: <a href="/projector/">use PizarraPad with a projector or TV</a>.</p>'''),

dict(slug='teach-math-on-projector', updated='2026-11-23',
     title='How to Teach Math on a Projector: Grids, Number Lines and Worked Examples',
     short='Teach math on a projector',
     desc='Practical ways to teach math on a classroom projector or TV with a digital board: grid pages, number lines, graphs, worked examples and student practice.',
     body='''<p class="lead">Math is easier to follow when students watch it being worked out, step by step. A digital board on the projector gives you a clean grid, colors and pages, without dusty chalk or a cramped whiteboard.</p>

<h2>Set up the board for math</h2>
<ul><li>Open <a href="/board/">PizarraPad</a> and choose the <b>Grid</b> background under <b>⋯</b>. The grid keeps columns of numbers lined up and makes graphs quick to draw.</li>
<li>Use the <b>greenboard</b> or <b>blackboard</b> on bright projectors; dark boards with light chalk colors are easiest to read from the back.</li>
<li>Use the <b>Thick</b> pen for numbers, and the <b>Medium</b> pen for small labels.</li></ul>

<h2>Worked examples, step by step</h2>
<p>Students learn a method by seeing each step and why it happens. On the board:</p>
<ol><li>Write the problem at the top of a fresh page.</li>
<li>Write each step on its own line, lined up on the grid.</li>
<li>Use one color for the working and another for the reason, for example “divide both sides by 3” in a second color beside the step.</li>
<li><b>Highlight</b> the answer, or draw a box around it with the <b>Shape</b> tool.</li>
<li>Start a new page for the next example. The finished example stays on the previous page if students want to look back.</li></ol>
<p>A useful routine is “I do, we do, you do”: you work the first example, the class tells you each step for the second, and students solve the third on their own while you walk around.</p>

<h2>Number lines</h2>
<ul><li>Draw a straight line with the <b>Shape</b> tool, using the arrow for direction.</li>
<li>Use the grid to space the marks evenly. Count squares rather than guessing.</li>
<li>Show jumps for addition and subtraction with curved pen strokes, in a bright color, and write the size of each jump above it.</li>
<li>For fractions and decimals, zoom in on part of the line and mark the smaller steps.</li></ul>

<h2>Graphs and coordinates</h2>
<ul><li>Draw the x and y axes with the arrow shape, then number them along the grid.</li>
<li>Plot points with small dots and label them, like A(2, 3).</li>
<li>Join points with straight lines from the <b>Shape</b> tool for linear graphs, or freehand for curves.</li>
<li>Use a different color for each line when comparing two graphs, and add a small key.</li></ul>

<h2>Geometry</h2>
<ul><li>Draw boxes and circles with the <b>Shape</b> tool, then label sides and angles.</li>
<li>Add a picture of a shape, a floor plan or a real object with the <b>Image</b> tool, and mark measurements on top of it.</li>
<li>Use the <b>laser</b> pointer to trace around a shape while you explain perimeter, without leaving marks.</li></ul>

<h2>Practice with the whole class</h2>
<ul><li><b>Mistake hunt:</b> work a problem with one deliberate error. Students find it and explain the fix.</li>
<li><b>Students at the board:</b> if you use a tablet, pass it to a student to solve a step while the class watches the big screen.</li>
<li><b>Quick check:</b> write three problems on a page, students solve them on paper, then reveal the answers one at a time.</li></ul>
<p>More ideas: <a href="https://telarlabs.net/guides/whiteboard-activities-projector-classroom/">whiteboard activities for the projector classroom</a>.</p>

<h2>After the lesson</h2>
<p>Save the worked examples with <b>⋯ → Save page as image</b> and share them with the class. Students who were absent, or who want to review before a test, can see every step exactly as you wrote it.</p>'''),

dict(slug='whiteboard-for-online-tutoring', updated='2026-11-23',
     title='How to Use an Online Whiteboard for Tutoring Over Zoom, Google Meet or Teams',
     short='Online whiteboard for tutoring over video calls',
     desc='Share a free online whiteboard in a video call: which window to share in Zoom, Google Meet and Microsoft Teams, writing with a tablet, and tips for clear lessons.',
     body='''<p class="lead">In online tutoring and classes, a board you can write on makes explanations much clearer than talking over slides. You can share PizarraPad in any video call app, because it’s just a browser tab.</p>

<h2>Step 1: Open the board</h2>
<p>Open <a href="/board/">PizarraPad</a> in your browser before the call. Choose a board and background under <b>⋯</b>. Light chalk colors on the <b>blackboard</b> or <b>greenboard</b> are easy to read on small phone screens; try a white board too, and keep whichever looks clearer in your call.</p>

<h2>Step 2: Share it in the call</h2>
<p>Share only the board, not your whole screen, so students don’t see your other tabs and notifications.</p>
<table class="tbl"><thead><tr><th>App</th><th>How to share the board</th></tr></thead><tbody>
<tr><td><b>Zoom</b></td><td>Press <b>Share screen</b> and choose the browser window with PizarraPad.</td></tr>
<tr><td><b>Google Meet</b></td><td>Press <b>Present now</b> (or the share screen button) and choose <b>A tab</b>, then the PizarraPad tab.</td></tr>
<tr><td><b>Microsoft Teams</b></td><td>Press <b>Share</b> and choose the window with PizarraPad.</td></tr></tbody></table>
<p>Video call apps change their buttons from time to time, but every one of them can share a window or a tab.</p>

<h2>Step 3: Choose how you’ll write</h2>
<ul><li><b>Mouse or trackpad:</b> fine for arrows, boxes and short labels. Use the <b>Text</b> tool to type longer notes; typed text is easier to read than mouse handwriting.</li>
<li><b>Tablet and stylus:</b> the best way to write naturally. Join the call on the tablet too, and share the tablet’s screen with PizarraPad open. Turn on <b>Pen only</b> so your palm doesn’t leave marks.</li>
<li><b>Drawing tablet:</b> a small, inexpensive pen tablet plugged into your laptop works like a pen for the mouse pointer.</li></ul>
<p>If you join the same call on two devices, mute the microphone and speaker on one of them to avoid echo.</p>

<h2>Tips for a clear online lesson</h2>
<ul><li><b>Write bigger than you think.</b> Students may be on a small phone screen. Use the Thick pen and Large text.</li>
<li><b>Use the laser pointer</b> to show where you are while you talk. Students can’t see your finger on the screen.</li>
<li><b>One idea per page.</b> Add pages with <b>+</b> instead of erasing. You can go back to an earlier page when a student asks.</li>
<li><b>Pause after writing.</b> Video can be a second or two behind. Give students time to see the step before you move on.</li>
<li><b>Add a picture</b> of the student’s homework or a textbook page with the <b>Image</b> tool, and mark it up together.</li></ul>

<h2>Step 4: Share the notes afterwards</h2>
<p>Save each page with <b>⋯ → Save page as image</b> and send the pictures in your chat or email after the session. Students then have the exact notes from the lesson to review, and parents can see what was covered.</p>

<h2>Privacy</h2>
<p>Your boards are saved only in your browser on your device. Nothing is uploaded to our servers, and there is no account. Only what you share in the call is seen by students.</p>
<p>Teaching in a classroom too? See <a href="/projector/">use PizarraPad with a projector or TV</a>.</p>'''),
]
