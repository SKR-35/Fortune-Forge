"""Content definitions used by the FortuneForge generator."""

from dataclasses import dataclass, field

from fortuneforge.domain import Language, Mood


@dataclass(frozen=True)
class ComponentValue:
    """One reusable phrase value with optional compatibility tags."""

    text: str
    tags: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class TemplateContent:
    """Reusable components for one controlled fortune template."""

    template: str
    components: dict[str, tuple[ComponentValue, ...]]


@dataclass(frozen=True)
class ContentPack:
    """Generation content for one language and mood."""

    language: Language
    mood: Mood
    templates: tuple[TemplateContent, ...]


ENGLISH_OPTIMISTIC = ContentPack(
    language=Language.ENGLISH,
    mood=Mood.OPTIMISTIC,
    templates=(
        TemplateContent(
            template="{time}, {event} will bring you {result}.",
            components={
                "time": (
                    ComponentValue("Soon"),
                    ComponentValue("Before long"),
                    ComponentValue("In the days ahead"),
                    ComponentValue("When you least expect it"),
                    ComponentValue("At just the right moment"),
                ),
                "event": (
                    ComponentValue("a small opportunity"),
                    ComponentValue("an unexpected conversation"),
                    ComponentValue("a well-timed decision"),
                    ComponentValue("a welcome invitation"),
                    ComponentValue("a change of routine"),
                    ComponentValue("a new connection"),
                ),
                "result": (
                    ComponentValue("good news"),
                    ComponentValue("a welcome surprise"),
                    ComponentValue("a reason to smile"),
                    ComponentValue("fresh confidence"),
                    ComponentValue("a useful discovery"),
                    ComponentValue("a brighter direction"),
                ),
            },
        ),
        TemplateContent(
            template="Your {quality} will lead you toward {outcome}.",
            components={
                "quality": (
                    ComponentValue("patience"),
                    ComponentValue("curiosity"),
                    ComponentValue("persistence"),
                    ComponentValue("kindness"),
                    ComponentValue("courage"),
                    ComponentValue("good judgment"),
                    ComponentValue("quiet confidence"),
                ),
                "outcome": (
                    ComponentValue("an unexpected opportunity"),
                    ComponentValue("a useful discovery"),
                    ComponentValue("a fortunate change"),
                    ComponentValue("a rewarding connection"),
                    ComponentValue("a satisfying result"),
                    ComponentValue("a promising new direction"),
                    ComponentValue("a moment worth remembering"),
                ),
            },
        ),
        TemplateContent(
            template="{action}, and {reward} may follow.",
            components={
                "action": (
                    ComponentValue("Trust your next thoughtful decision"),
                    ComponentValue("Keep moving toward what matters"),
                    ComponentValue("Give a new idea some room"),
                    ComponentValue("Take the opportunity in front of you"),
                    ComponentValue("Stay open to an unexpected possibility"),
                    ComponentValue("Follow the path that feels quietly promising"),
                ),
                "reward": (
                    ComponentValue("good news"),
                    ComponentValue("a pleasant surprise"),
                    ComponentValue("new confidence"),
                    ComponentValue("a useful opportunity"),
                    ComponentValue("a fortunate turn"),
                    ComponentValue("something worth celebrating"),
                ),
            },
        ),
        TemplateContent(
            template="A {thing} may soon become {benefit}.",
            components={
                "thing": (
                    ComponentValue("small change"),
                    ComponentValue("new idea"),
                    ComponentValue("chance meeting"),
                    ComponentValue("steady effort"),
                    ComponentValue("simple decision"),
                    ComponentValue("new beginning"),
                ),
                "benefit": (
                    ComponentValue("the start of something rewarding"),
                    ComponentValue("more valuable than it first appears"),
                    ComponentValue("a source of unexpected happiness"),
                    ComponentValue("an opportunity in disguise"),
                    ComponentValue("a reason for renewed confidence"),
                    ComponentValue("the answer to an old question"),
                ),
            },
        ),
        TemplateContent(
            template="{opening}; {prediction}.",
            components={
                "opening": (
                    ComponentValue("Keep your eyes open"),
                    ComponentValue("Trust the progress you cannot yet see"),
                    ComponentValue("Leave a little room for surprise"),
                    ComponentValue("Do not underestimate small beginnings"),
                    ComponentValue("Stay curious about what comes next"),
                    ComponentValue("Let patience work in your favor"),
                ),
                "prediction": (
                    ComponentValue("something encouraging is taking shape"),
                    ComponentValue("a useful opportunity is drawing closer"),
                    ComponentValue("good news may arrive from an unexpected direction"),
                    ComponentValue("a difficult question will become easier"),
                    ComponentValue("your next step will reveal more than you expect"),
                    ComponentValue("a fortunate coincidence may soon make sense"),
                ),
            },
        ),
        TemplateContent(
            template="{sign} could be the beginning of {outcome}.",
            components={
                "sign": (
                    ComponentValue("A small success"),
                    ComponentValue("An unexpected message"),
                    ComponentValue("A new possibility"),
                    ComponentValue("A change in plans"),
                    ComponentValue("A helpful conversation"),
                    ComponentValue("A moment of clarity"),
                    ComponentValue("A fresh idea"),
                ),
                "outcome": (
                    ComponentValue("something much bigger"),
                    ComponentValue("a rewarding new chapter"),
                    ComponentValue("a welcome change"),
                    ComponentValue("an opportunity worth pursuing"),
                    ComponentValue("a surprisingly good outcome"),
                    ComponentValue("a path you will be glad you followed"),
                    ComponentValue("a happier turn of events"),
                ),
            },
        ),
        TemplateContent(
            template="{time}, you may discover that {realization}.",
            components={
                "time": (
                    ComponentValue("Soon"),
                    ComponentValue("Before long"),
                    ComponentValue("In the coming days"),
                    ComponentValue("At an unexpected moment"),
                    ComponentValue("When the timing is right"),
                    ComponentValue("Earlier than you expect"),
                    ComponentValue("After a little patience"),
                ),
                "realization": (
                    ComponentValue("your effort has been noticed"),
                    ComponentValue("a difficult choice has a simple answer"),
                    ComponentValue("an old worry no longer matters"),
                    ComponentValue("a new direction suits you well"),
                    ComponentValue("someone has good news for you"),
                    ComponentValue("your patience was worth it"),
                    ComponentValue("you are closer to your goal than you thought"),
                ),
            },
        ),
        TemplateContent(
            template="Your next {choice} may open the way to {reward}.",
            components={
                "choice": (
                    ComponentValue("careful decision"),
                    ComponentValue("bold step"),
                    ComponentValue("kind gesture"),
                    ComponentValue("new idea"),
                    ComponentValue("honest conversation"),
                    ComponentValue("change of direction"),
                    ComponentValue("small act of courage"),
                    ComponentValue("patient move"),
                    ComponentValue("thoughtful risk"),
                    ComponentValue("fresh approach"),
                ),
                "reward": (
                    ComponentValue("an unexpected opportunity"),
                    ComponentValue("a satisfying result"),
                    ComponentValue("a valuable connection"),
                    ComponentValue("a welcome improvement"),
                    ComponentValue("something worth celebrating"),
                    ComponentValue("a fortunate discovery"),
                    ComponentValue("a brighter possibility"),
                    ComponentValue("a long-awaited answer"),
                    ComponentValue("renewed hope"),
                ),
            },
        ),
    ),
)

ENGLISH_HUMOROUS = ContentPack(
    language=Language.ENGLISH,
    mood=Mood.HUMOROUS,
    templates=(
        # Fortune-cookie absurdity
        TemplateContent(
            template="{prediction}; {twist}.",
            components={
                "prediction": (
                    ComponentValue("A mysterious opportunity is approaching"),
                    ComponentValue("Good fortune is heading your way"),
                    ComponentValue("An unexpected answer will soon appear"),
                    ComponentValue("A bold decision is waiting for you"),
                    ComponentValue("A pleasant surprise is getting closer"),
                    ComponentValue("A lucky coincidence is on its way"),
                    ComponentValue("An unusual invitation may arrive soon"),
                    ComponentValue("Something unexpectedly useful will find you"),
                ),
                "twist": (
                    ComponentValue("it may be lunch"),
                    ComponentValue("keep the receipt"),
                    ComponentValue("try to look surprised"),
                    ComponentValue("tomorrow is also available"),
                    ComponentValue("do not spend it all in one place"),
                    ComponentValue("its timing remains suspicious"),
                    ComponentValue("act like this was your plan"),
                    ComponentValue("snacks may be involved"),
                ),
            },
        ),
        # Advice with a playful reversal
        TemplateContent(
            template="{advice}, except {exception}.",
            components={
                "advice": (
                    ComponentValue("Trust your instincts"),
                    ComponentValue("Follow your curiosity"),
                    ComponentValue("Listen to your inner voice"),
                    ComponentValue("Take the brave option"),
                    ComponentValue("Believe in your judgment"),
                    ComponentValue("Stay open to possibilities"),
                    ComponentValue("Be generous with second chances"),
                    ComponentValue("Keep an open mind"),
                ),
                "exception": (
                    ComponentValue("when it recommends a third dessert"),
                    ComponentValue("when you are looking for your keys"),
                    ComponentValue("when online shopping is involved"),
                    ComponentValue("when everyone else suddenly becomes very quiet"),
                    ComponentValue('when the instructions say "easy assembly"'),
                    ComponentValue("when your phone is at one percent"),
                    ComponentValue('when someone says "this will only take a minute"'),
                    ComponentValue("when the cat looks unusually confident"),
                ),
            },
        ),
        # Everyday objects
        TemplateContent(
            template="{object} may soon {action}.",
            components={
                "object": (
                    ComponentValue("Your refrigerator"),
                    ComponentValue("Your alarm clock"),
                    ComponentValue("Your left shoe"),
                    ComponentValue("Your favorite mug"),
                    ComponentValue("The nearest chair"),
                    ComponentValue("Your umbrella"),
                    ComponentValue("Your house keys"),
                    ComponentValue("The mysterious drawer everyone has"),
                ),
                "action": (
                    ComponentValue("become unexpectedly important"),
                    ComponentValue("question one of your recent decisions"),
                    ComponentValue("know more than it is willing to admit"),
                    ComponentValue("demand the respect it deserves"),
                    ComponentValue("solve a problem nobody asked it to solve"),
                    ComponentValue("remind you who is really in charge"),
                    ComponentValue("appear exactly where you already looked"),
                    ComponentValue("develop suspiciously strong opinions"),
                ),
            },
        ),
        # Social fortunes
        TemplateContent(
            template="{person}; {reveal}.",
            components={
                "person": (
                    ComponentValue("Someone is thinking about you"),
                    ComponentValue("A stranger may soon remember your face"),
                    ComponentValue("An old friend may contact you"),
                    ComponentValue("Someone nearby admires your confidence"),
                    ComponentValue("A helpful person may appear unexpectedly"),
                    ComponentValue("Someone may soon ask for your opinion"),
                    ComponentValue("A familiar face may bring surprising news"),
                    ComponentValue("Someone you trust may offer useful advice"),
                ),
                "reveal": (
                    ComponentValue("they may also need a favor"),
                    ComponentValue("pretend this prediction never happened"),
                    ComponentValue("there is probably a story behind it"),
                    ComponentValue("you are allowed to look mysterious"),
                    ComponentValue("ask about the snacks before committing"),
                    ComponentValue("choose your dramatic pause carefully"),
                    ComponentValue("the details may be less impressive"),
                    ComponentValue("nod wisely until more information arrives"),
                ),
            },
        ),
        # Food / fortune-cookie humor
        TemplateContent(
            template="{food_fortune}; {food_twist}.",
            components={
                "food_fortune": (
                    ComponentValue("A delicious opportunity awaits"),
                    ComponentValue("Your next meal may contain an important clue"),
                    ComponentValue("Great wisdom will arrive around lunchtime"),
                    ComponentValue("A snack may improve your next decision"),
                    ComponentValue("Good news tastes better on a full stomach"),
                    ComponentValue("A difficult problem may surrender to dessert"),
                    ComponentValue("Your fortunes improve near baked goods"),
                    ComponentValue("A wise choice may soon appear on a menu"),
                ),
                "food_twist": (
                    ComponentValue("ordering two is still technically a choice"),
                    ComponentValue("fortune cookies are rarely neutral witnesses"),
                    ComponentValue("save room for unexpected developments"),
                    ComponentValue("sharing remains optional"),
                    ComponentValue("calories have declined to comment"),
                    ComponentValue("the last piece knows who wants it"),
                    ComponentValue("your future self supports this research"),
                    ComponentValue("napkins may become strategically important"),
                ),
            },
        ),
        # Luck
        TemplateContent(
            template="{luck}; {caution}.",
            components={
                "luck": (
                    ComponentValue("Your luck is changing"),
                    ComponentValue("A lucky break may arrive soon"),
                    ComponentValue("Fortune appears to be on your side"),
                    ComponentValue("A small streak of luck is beginning"),
                    ComponentValue("The odds may briefly favor you"),
                    ComponentValue("Something fortunate is quietly developing"),
                    ComponentValue("A coincidence may work in your favor"),
                    ComponentValue("Today has unusual potential"),
                ),
                "caution": (
                    ComponentValue("keep the receipt"),
                    ComponentValue("do not frighten it away"),
                    ComponentValue("avoid explaining it too confidently"),
                    ComponentValue("results may vary after midnight"),
                    ComponentValue("the universe dislikes showing off"),
                    ComponentValue("try not to immediately test your limits"),
                    ComponentValue("use responsibly"),
                    ComponentValue("no warranty is implied"),
                ),
            },
        ),
        # Daily-life absurdity
        TemplateContent(
            template="{event} will teach you {lesson}.",
            components={
                "event": (
                    ComponentValue("A missing sock"),
                    ComponentValue("An unexpected nap"),
                    ComponentValue("A stubborn jar lid"),
                    ComponentValue("A wrong turn"),
                    ComponentValue("An unusually long queue"),
                    ComponentValue("A forgotten umbrella"),
                    ComponentValue("A mysterious noise"),
                    ComponentValue("A door that refuses to cooperate"),
                ),
                "lesson": (
                    ComponentValue("that confidence is not the same as a plan"),
                    ComponentValue("the value of selective optimism"),
                    ComponentValue("why patience has a sense of humor"),
                    ComponentValue("that dignity is occasionally optional"),
                    ComponentValue("the importance of pretending this was intentional"),
                    ComponentValue("that small victories deserve recognition"),
                    ComponentValue("why backup plans need backup plans"),
                    ComponentValue("that timing is mostly a rumor"),
                ),
            },
        ),
        # Limited work/technology humor — deliberately only one family
        TemplateContent(
            template="{work_event}; {work_twist}.",
            components={
                "work_event": (
                    ComponentValue("Your next meeting may be surprisingly useful"),
                    ComponentValue("A suspiciously short email may arrive"),
                    ComponentValue("Your next spreadsheet may contain good news"),
                    ComponentValue("A technical problem may solve itself"),
                    ComponentValue("Someone may finally read the instructions"),
                    ComponentValue("Your inbox may briefly show mercy"),
                    ComponentValue("A deadline may become unexpectedly reasonable"),
                    ComponentValue("The printer may cooperate"),
                ),
                "work_twist": (
                    ComponentValue("document this rare event"),
                    ComponentValue("remain calm"),
                    ComponentValue("nobody needs to know how surprised you are"),
                    ComponentValue("do not make sudden movements"),
                    ComponentValue("enjoy it before the next notification"),
                    ComponentValue("coffee may still be required"),
                    ComponentValue("this phenomenon may not be reproducible"),
                    ComponentValue("scientists remain cautious"),
                ),
            },
        ),
        # Compatibility-aware humor:
        # punchlines only combine with matching setup categories.
        TemplateContent(
            template="{setup}; {punchline}.",
            components={
                "setup": (
                    ComponentValue(
                        "Your pet may understand more than you think",
                        frozenset({"provides:animal"}),
                    ),
                    ComponentValue(
                        "An animal may influence your next decision",
                        frozenset({"provides:animal"}),
                    ),
                    ComponentValue(
                        "The nearest cat appears to know something",
                        frozenset({"provides:animal"}),
                    ),
                    ComponentValue(
                        "Your next meal may reveal hidden wisdom",
                        frozenset({"provides:food"}),
                    ),
                    ComponentValue(
                        "Dessert may play an important role today",
                        frozenset({"provides:food"}),
                    ),
                    ComponentValue(
                        "A snack may soon change your perspective",
                        frozenset({"provides:food"}),
                    ),
                    ComponentValue(
                        "The weather has plans for you",
                        frozenset({"provides:weather"}),
                    ),
                    ComponentValue(
                        "An unexpected breeze may bring clarity",
                        frozenset({"provides:weather"}),
                    ),
                    ComponentValue(
                        "Today's forecast contains a surprise",
                        frozenset({"provides:weather"}),
                    ),
                    ComponentValue(
                        "Sleep may answer a question you have been avoiding",
                        frozenset({"provides:sleep"}),
                    ),
                    ComponentValue(
                        "Your pillow may offer excellent advice tonight",
                        frozenset({"provides:sleep"}),
                    ),
                    ComponentValue(
                        "A nap may become unexpectedly productive",
                        frozenset({"provides:sleep"}),
                    ),
                ),
                "punchline": (
                    ComponentValue(
                        "consider negotiating with treats",
                        frozenset({"requires:animal"}),
                    ),
                    ComponentValue(
                        "do not let it manage your finances",
                        frozenset({"requires:animal"}),
                    ),
                    ComponentValue(
                        "its confidence is not evidence",
                        frozenset({"requires:animal"}),
                    ),
                    ComponentValue(
                        "take notes before ordering seconds",
                        frozenset({"requires:food"}),
                    ),
                    ComponentValue(
                        "the sauce may contain additional information",
                        frozenset({"requires:food"}),
                    ),
                    ComponentValue(
                        "research may require another serving",
                        frozenset({"requires:food"}),
                    ),
                    ComponentValue(
                        "carry an umbrella and lower your expectations",
                        frozenset({"requires:weather"}),
                    ),
                    ComponentValue(
                        "the clouds refuse to provide details",
                        frozenset({"requires:weather"}),
                    ),
                    ComponentValue(
                        "meteorology denies responsibility",
                        frozenset({"requires:weather"}),
                    ),
                    ComponentValue(
                        "consult it again after eight hours",
                        frozenset({"requires:sleep"}),
                    ),
                    ComponentValue(
                        "answers may arrive with drool",
                        frozenset({"requires:sleep"}),
                    ),
                    ComponentValue(
                        "do not schedule anything important during the experiment",
                        frozenset({"requires:sleep"}),
                    ),
                ),
            },
        ),
    ),
)

ENGLISH_PESSIMISTIC = ContentPack(
    language=Language.ENGLISH,
    mood=Mood.PESSIMISTIC,
    templates=(
        TemplateContent(
            template="{prediction}; {downside}.",
            components={
                "prediction": (
                    ComponentValue("Good news may arrive"),
                    ComponentValue("A solution may appear"),
                    ComponentValue("A useful opportunity may come"),
                    ComponentValue("Someone may finally agree with you"),
                    ComponentValue("Your plan may begin to work"),
                    ComponentValue("A small success may be close"),
                    ComponentValue("A promising idea may survive"),
                    ComponentValue("A quiet improvement may begin"),
                ),
                "downside": (
                    ComponentValue("probably after it would have been most useful"),
                    ComponentValue("expect additional paperwork"),
                    ComponentValue("the timing may still be disappointing"),
                    ComponentValue("someone will likely complicate it"),
                    ComponentValue("there may be conditions attached"),
                    ComponentValue("do not celebrate too early"),
                    ComponentValue("the easy part is probably over"),
                    ComponentValue("some patience will still be required"),
                ),
            },
        ),
        TemplateContent(
            template="{event} will remind you that {lesson}.",
            components={
                "event": (
                    ComponentValue("A simple task"),
                    ComponentValue("A minor delay"),
                    ComponentValue("An ordinary conversation"),
                    ComponentValue("A missing detail"),
                    ComponentValue("A small mistake"),
                    ComponentValue("An unexpected request"),
                    ComponentValue("A routine decision"),
                    ComponentValue("A harmless assumption"),
                ),
                "lesson": (
                    ComponentValue("nothing is ever quite as simple as advertised"),
                    ComponentValue("timing has a sense of humor"),
                    ComponentValue("confidence is not evidence"),
                    ComponentValue("small problems enjoy company"),
                    ComponentValue("the obvious answer sometimes arrives last"),
                    ComponentValue("plans rarely read their own instructions"),
                    ComponentValue("patience is usually requested without notice"),
                    ComponentValue("certainty tends to expire quickly"),
                ),
            },
        ),
        TemplateContent(
            template="{advice}; {warning}.",
            components={
                "advice": (
                    ComponentValue("Lower your expectations slightly"),
                    ComponentValue("Keep a backup plan nearby"),
                    ComponentValue("Double-check the simple part"),
                    ComponentValue("Leave extra time"),
                    ComponentValue("Read the fine print"),
                    ComponentValue("Prepare for one more step"),
                    ComponentValue("Keep your confidence flexible"),
                    ComponentValue("Do not assume the easy option is available"),
                ),
                "warning": (
                    ComponentValue("today may insist on being educational"),
                    ComponentValue("the details may be less encouraging"),
                    ComponentValue("someone may change the plan"),
                    ComponentValue("the shortcut may take longer"),
                    ComponentValue("the obvious solution may be unavailable"),
                    ComponentValue("a small inconvenience may become ambitious"),
                    ComponentValue("your schedule may disagree"),
                    ComponentValue("the universe has not confirmed anything"),
                ),
            },
        ),
        TemplateContent(
            template="Your {quality} may be tested by {obstacle}.",
            components={
                "quality": (
                    ComponentValue("patience"),
                    ComponentValue("optimism"),
                    ComponentValue("good judgment"),
                    ComponentValue("sense of humor"),
                    ComponentValue("attention to detail"),
                    ComponentValue("ability to improvise"),
                    ComponentValue("careful planning"),
                    ComponentValue("confidence"),
                ),
                "obstacle": (
                    ComponentValue("something remarkably unimportant"),
                    ComponentValue("an avoidable delay"),
                    ComponentValue("a confusing instruction"),
                    ComponentValue("someone else's certainty"),
                    ComponentValue("a problem that nearly solved itself"),
                    ComponentValue("a missing piece of information"),
                    ComponentValue("an inconvenient coincidence"),
                    ComponentValue("a task with one step too many"),
                ),
            },
        ),
        TemplateContent(
            template="{situation} may turn out to be {outcome}.",
            components={
                "situation": (
                    ComponentValue("The promising option"),
                    ComponentValue("The easy solution"),
                    ComponentValue("The sensible plan"),
                    ComponentValue("The quick answer"),
                    ComponentValue("The obvious choice"),
                    ComponentValue("The convenient route"),
                    ComponentValue("The simple explanation"),
                    ComponentValue("The reassuring message"),
                ),
                "outcome": (
                    ComponentValue("more complicated than expected"),
                    ComponentValue("less helpful than advertised"),
                    ComponentValue("temporarily unavailable"),
                    ComponentValue("someone else's problem first"),
                    ComponentValue("only mostly correct"),
                    ComponentValue("surprisingly expensive"),
                    ComponentValue("dependent on one missing detail"),
                    ComponentValue("the beginning of another question"),
                ),
            },
        ),
        TemplateContent(
            template="{time}, {problem} may {result}.",
            components={
                "time": (
                    ComponentValue("Soon"),
                    ComponentValue("Before long"),
                    ComponentValue("Later than expected"),
                    ComponentValue("At an inconvenient moment"),
                    ComponentValue("When things seem settled"),
                    ComponentValue("Just as you relax"),
                    ComponentValue("After unnecessary discussion"),
                    ComponentValue("When you think you are finished"),
                ),
                "problem": (
                    ComponentValue("a small complication"),
                    ComponentValue("an overlooked detail"),
                    ComponentValue("a minor delay"),
                    ComponentValue("an unexpected question"),
                    ComponentValue("a forgotten task"),
                    ComponentValue("a routine problem"),
                    ComponentValue("a harmless misunderstanding"),
                    ComponentValue("a last-minute change"),
                ),
                "result": (
                    ComponentValue("require more patience than expected"),
                    ComponentValue("take longer than it should"),
                    ComponentValue("create one additional problem"),
                    ComponentValue("interrupt an otherwise reasonable day"),
                    ComponentValue("need an unnecessarily careful answer"),
                    ComponentValue("make the obvious solution less obvious"),
                    ComponentValue("arrive with poor timing"),
                    ComponentValue("refuse to stay small"),
                ),
            },
        ),
    ),
)

ENGLISH_OMINOUS = ContentPack(
    language=Language.ENGLISH,
    mood=Mood.OMINOUS,
    templates=(
        TemplateContent(
            template="{warning}; {twist}.",
            components={
                "warning": (
                    ComponentValue("Listen carefully when the room goes quiet"),
                    ComponentValue("Pay attention to the second knock"),
                    ComponentValue("Do not ignore an unfamiliar reflection"),
                    ComponentValue("Remember where you left the key"),
                    ComponentValue("Notice which clock stops first"),
                    ComponentValue("Watch the doorway when the lights flicker"),
                    ComponentValue("Take note if your shadow seems late"),
                    ComponentValue("Be cautious when everything suddenly feels familiar"),
                ),
                "twist": (
                    ComponentValue("some silences are unusually observant"),
                    ComponentValue("coincidences dislike being questioned"),
                    ComponentValue("the house may simply be remembering something"),
                    ComponentValue("not every answer improves the question"),
                    ComponentValue("the night has excellent timing"),
                    ComponentValue("ordinary things sometimes practice being mysterious"),
                    ComponentValue("your imagination may have company"),
                    ComponentValue("the explanation may be less comforting than the mystery"),
                ),
            },
        ),
        TemplateContent(
            template="{object} may soon {behavior}.",
            components={
                "object": (
                    ComponentValue("The oldest mirror nearby"),
                    ComponentValue("A forgotten photograph"),
                    ComponentValue("The quietest clock in the room"),
                    ComponentValue("A door you rarely use"),
                    ComponentValue("An empty chair"),
                    ComponentValue("A misplaced key"),
                    ComponentValue("A familiar hallway"),
                    ComponentValue("The last light you switch off"),
                ),
                "behavior": (
                    ComponentValue("seem more familiar than it should"),
                    ComponentValue("remember something you do not"),
                    ComponentValue("become strangely difficult to ignore"),
                    ComponentValue("appear to be waiting for better timing"),
                    ComponentValue("raise a question nobody asked"),
                    ComponentValue("feel slightly out of place"),
                    ComponentValue("make an ordinary moment unusually quiet"),
                    ComponentValue("offer no useful explanation whatsoever"),
                ),
            },
        ),
        TemplateContent(
            template="{time}, {event} may {result}.",
            components={
                "time": (
                    ComponentValue("Tonight"),
                    ComponentValue("Before morning"),
                    ComponentValue("When the house is quiet"),
                    ComponentValue("At an inconvenient hour"),
                    ComponentValue("When you least expect it"),
                    ComponentValue("Just after midnight"),
                    ComponentValue("The next time you are alone"),
                    ComponentValue("When the weather suddenly changes"),
                ),
                "event": (
                    ComponentValue("a familiar sound"),
                    ComponentValue("an unexplained shadow"),
                    ComponentValue("a forgotten memory"),
                    ComponentValue("a small coincidence"),
                    ComponentValue("an ordinary reflection"),
                    ComponentValue("a distant noise"),
                    ComponentValue("an unexpected draft"),
                    ComponentValue("a strangely timed light"),
                ),
                "result": (
                    ComponentValue("seem more important than usual"),
                    ComponentValue("arrive from the wrong direction"),
                    ComponentValue("make perfect sense for the wrong reason"),
                    ComponentValue("leave you with one question too many"),
                    ComponentValue("feel oddly well timed"),
                    ComponentValue("refuse to remain ordinary"),
                    ComponentValue("suggest that someone forgot to explain something"),
                    ComponentValue("make tomorrow seem slightly farther away"),
                ),
            },
        ),
        TemplateContent(
            template="{omen}; {interpretation}.",
            components={
                "omen": (
                    ComponentValue("A light may flicker without explanation"),
                    ComponentValue("A clock may lose exactly one minute"),
                    ComponentValue("A door may close more quietly than expected"),
                    ComponentValue("A familiar song may sound slightly different"),
                    ComponentValue("A shadow may seem unusually patient"),
                    ComponentValue("A name may appear twice today"),
                    ComponentValue("A forgotten object may return"),
                    ComponentValue("A harmless coincidence may repeat itself"),
                ),
                "interpretation": (
                    ComponentValue("pretend not to notice"),
                    ComponentValue("the universe enjoys subtlety"),
                    ComponentValue("this is probably fine"),
                    ComponentValue("probably"),
                    ComponentValue("do not demand an explanation too quickly"),
                    ComponentValue("some mysteries become annoyed when rushed"),
                    ComponentValue("there is no need to panic yet"),
                    ComponentValue("write it down before memory becomes creative"),
                ),
            },
        ),
        TemplateContent(
            template="{advice}, especially if {condition}.",
            components={
                "advice": (
                    ComponentValue("Keep one light on"),
                    ComponentValue("Remember which door you closed"),
                    ComponentValue("Trust your memory cautiously"),
                    ComponentValue("Count the footsteps only once"),
                    ComponentValue("Do not argue with a strange coincidence"),
                    ComponentValue("Keep the old key somewhere safe"),
                    ComponentValue("Leave unexplained noises unexplained"),
                    ComponentValue("Avoid asking mirrors difficult questions"),
                ),
                "condition": (
                    ComponentValue("the hallway seems longer than yesterday"),
                    ComponentValue("the clock insists it is earlier than it is"),
                    ComponentValue("you hear something twice"),
                    ComponentValue("the room suddenly feels occupied"),
                    ComponentValue("your reflection looks more confident than you"),
                    ComponentValue("the cat refuses to enter first"),
                    ComponentValue("the lights behave as if they know something"),
                    ComponentValue("someone mentions a dream you almost remember"),
                ),
            },
        ),
        TemplateContent(
            template="{observation}; {dark_humor}.",
            components={
                "observation": (
                    ComponentValue("Something feels slightly unusual tonight"),
                    ComponentValue("The room seems quieter than necessary"),
                    ComponentValue("Your shadow appears unusually cooperative"),
                    ComponentValue("The night is going suspiciously well"),
                    ComponentValue("Nothing strange has happened yet"),
                    ComponentValue("Everything seems perfectly normal"),
                    ComponentValue("The silence feels unusually organized"),
                    ComponentValue("The house appears to be minding its own business"),
                ),
                "dark_humor": (
                    ComponentValue("give it time"),
                    ComponentValue("this may be the suspicious part"),
                    ComponentValue("avoid congratulating yourself too early"),
                    ComponentValue("the evening is still young"),
                    ComponentValue("remain professionally concerned"),
                    ComponentValue("your optimism has been noted"),
                    ComponentValue("statistics offer limited comfort"),
                    ComponentValue("no warranty is implied"),
                ),
            },
        ),
        TemplateContent(
            template="{prediction}; {qualification}.",
            components={
                "prediction": (
                    ComponentValue("An old question may return"),
                    ComponentValue("A forgotten detail may become important"),
                    ComponentValue("A strange coincidence may repeat"),
                    ComponentValue("Something misplaced may reappear"),
                    ComponentValue("A quiet mystery may become less quiet"),
                    ComponentValue("A familiar place may feel unfamiliar"),
                    ComponentValue("A forgotten warning may suddenly make sense"),
                    ComponentValue("An ordinary night may become memorable"),
                ),
                "qualification": (
                    ComponentValue("not necessarily in a helpful way"),
                    ComponentValue("timing remains uncertain"),
                    ComponentValue("the details may prefer to stay mysterious"),
                    ComponentValue("answers are not guaranteed"),
                    ComponentValue("you may wish you had taken notes"),
                    ComponentValue("interpretation is entirely your problem"),
                    ComponentValue("the universe declines further comment"),
                    ComponentValue("sleep may become optional"),
                ),
            },
        ),
        TemplateContent(
            template="{sensation} may mean {meaning}.",
            components={
                "sensation": (
                    ComponentValue("A sudden chill"),
                    ComponentValue("A familiar smell with no obvious source"),
                    ComponentValue("The feeling that you forgot something"),
                    ComponentValue("A sound from an empty room"),
                    ComponentValue("A brief sense of déjà vu"),
                    ComponentValue("An unexplained pause in conversation"),
                    ComponentValue("A light that seems slightly too dim"),
                    ComponentValue("The urge to check the hallway twice"),
                ),
                "meaning": (
                    ComponentValue("nothing at all, which is somehow worse"),
                    ComponentValue("the timing is becoming interesting"),
                    ComponentValue("your imagination has excellent instincts"),
                    ComponentValue("someone forgot to finish the explanation"),
                    ComponentValue("the night is paying attention"),
                    ComponentValue("a coincidence has become ambitious"),
                    ComponentValue("ordinary reality is taking a short break"),
                    ComponentValue("you should probably keep the receipt"),
                ),
            },
        ),
        TemplateContent(
            template="{if_clause}; {response}.",
            components={
                "if_clause": (
                    ComponentValue("If you feel watched"),
                    ComponentValue("If the mirror seems unusually attentive"),
                    ComponentValue("If the same sound returns"),
                    ComponentValue("If the hallway seems slightly different"),
                    ComponentValue("If an empty room feels less empty"),
                    ComponentValue("If the lights flicker twice"),
                    ComponentValue("If you hear your name unexpectedly"),
                    ComponentValue("If a familiar object appears somewhere new"),
                ),
                "response": (
                    ComponentValue("do not turn around too dramatically"),
                    ComponentValue("remain calm and blame the architecture"),
                    ComponentValue("pretend this is completely ordinary"),
                    ComponentValue("consider postponing curiosity until morning"),
                    ComponentValue("mirrors are notoriously difficult witnesses"),
                    ComponentValue("the universe may simply be bored"),
                    ComponentValue("your imagination would appreciate some credit"),
                    ComponentValue("a confident exit remains a valid strategy"),
                ),
            },
        ),
        TemplateContent(
            template="{closing}; {afterthought}.",
            components={
                "closing": (
                    ComponentValue("Sleep peacefully tonight"),
                    ComponentValue("Try not to worry"),
                    ComponentValue("Everything will probably be fine"),
                    ComponentValue("There is little reason for concern"),
                    ComponentValue("The night should pass normally"),
                    ComponentValue("You may rest without suspicion"),
                    ComponentValue("Tomorrow will likely arrive as expected"),
                    ComponentValue("Remain optimistic"),
                ),
                "afterthought": (
                    ComponentValue("probably"),
                    ComponentValue("unless the clock stops again"),
                    ComponentValue("assuming nobody knocks twice"),
                    ComponentValue("provided the hallway remains the same length"),
                    ComponentValue("the mirror has made no promises"),
                    ComponentValue("results may vary after midnight"),
                    ComponentValue("the shadows have not objected"),
                    ComponentValue("for now"),
                ),
            },
        ),
    ),
)


CONTENT_PACKS: dict[tuple[Language, Mood], ContentPack] = {
    (Language.ENGLISH, Mood.OPTIMISTIC): ENGLISH_OPTIMISTIC,
    (Language.ENGLISH, Mood.HUMOROUS): ENGLISH_HUMOROUS,
    (Language.ENGLISH, Mood.PESSIMISTIC): ENGLISH_PESSIMISTIC,
    (Language.ENGLISH, Mood.OMINOUS): ENGLISH_OMINOUS,
}


def get_content_pack(language: Language, mood: Mood) -> ContentPack:
    """Return the content pack for the requested language and mood."""
    try:
        return CONTENT_PACKS[(language, mood)]
    except KeyError as exc:
        raise LookupError(f"No content pack exists for {language.value} / {mood.value}.") from exc
