/*
PROBLEM SET ONE
--------------------------------------------------
NAME:Christine Jin
ID: B20855407
HOURS TO COMPLETE:4hrs
KEY: 0x423AE192
*/

/*
WARMUP 1: Order of Operations

In math, PEMDAS (parentheses, exponents, multiplication, division, addition, subtraction)
defines the order of operations to compute mathematical expressions.  For example,
the following expression 11 + 12 * ((7 / 3) - 1) evaluates to 27.  sclang evaluates
mathematical expressions from left to right.  There is no precedence of operators like
PEMDAS.  Precedence, however, can be forced with parentheses in sclang.  Rearrange the
mathematical example above WITHOUT parentheses (i.e., use exactly one instance of the
following operands 11, 12, 7, 3, 1 and the operators +, *, /, - ) to compute 27 in sclang.
Note that you cannot do something like 3 * 7 + 7 - 1 = 27 because the operand 7 is used more
than once and the expression lacks operands 11 and 12 and the / operator.  Set the expression
equal to ~result.  For example, your final answer might be ~result = 1 - 11 + 12 * 7 / 3.
This, of course, is incorrect because ~result = 4.6666.
*/

(
~result = 7/3 - 1 * 12 + 11;
~result.postln;
)

/*
WARMUP 2: Exclamations

Write a simple function that accepts a string like "hello" and returns a new string with
exclamation points appended. The number of exclamation points is determined by the index.  For
example, ~exclamation.value("hello", 3) yields "hello!!!".  You can assume the input string is
in fact a string and that the index is a non-negative integer.  Note, two strings can be
concatenated together with the ++ operator.
*/

(
~exclamation = {
	arg str, index;
	while ({index > 0}, {str = str ++ "!"; index = index - 1});
	str;
};
)

~exclamation.value("hello", 3).postln; // Should post hello!!!
~exclamation.value("", 1).postln; // Should post !
~exclamation.value("andy", 0).postln; // Should post andy

// Add your own testing here if you like

/*
WARMUP 3: Data Access

Consider the data structure ~data built below.  Write three assignment statements that
access pieces of that data structure.

~one -> write an expression that retrieves the number 1 from the data structure
~a -> write an expression that retrieves the letter "a" from the data structure
~isThree -> write an expression that tests whether 3 is part of the set in the data structure
*/

(
~data = Dictionary[];
~data.put(\array, [1, 2, ["a"]]);
~data.put(\set, Set[3, 4]);
)

~one = ~data[\array][0]; // Expression should result in 1
~a = ~data[\array][2][0]; // Expression should result in a
~isThree = if (~data[\set].includes(3), true, false);// Expression should result in true

/*
WARMUP 4: Favorite Numbers

Consider a dictionary of keys that are strings representing people and values
that are non-negative integers representing those people's favorite numbers.
Write a function that posts the names of everyone whose favorite number is
a single digit like 4 or 7.  Each name should be posted on a separate line.
*/

(
~dictIterate = {
	arg dict;
	dict.keysValuesDo({|key, value|
		if (value < 10, {key.postln});
	});

}
)

~testDict = Dictionary.newFrom(["andy", 4, "rigel", 3, "katherine", 12, "parker", 42]);
~dictIterate.value(~testDict); // Should post andy and rigel but not katherine or parker






/*
FUNCTIONAL FUN: Transposition

Define a function that takes a list of notes and returns a new list of those numbers translated
by a specific semitone.  A note is defined as a single non-negative integer where the value of
the integer represents its pitch.  We will be adhering to the MIDI protocol which specifies that
concert A is the number 69.  We will be learning much more about MIDI as the semester progresses.

The MIDI protocol specifies that we have 128 notes between 0 and 127 inclusive.  A full 88-key
piano in the MIDI system comprises the notes 21 to 108 inclusive.  To transpose a note n by x
number of semitones, simply compute x + n.  If any of the notes fall out of the acceptable range
of notes (i.e., below zero or above 127), then the function should return nil.

Note that a function in SuperCollider returns the last expression.  Your function should return
immediately after finding a note out-of-range and not continue to tranpose subsequent notes.
Inconveniently, SuperCollider does not have a notion of early return like Python does.  It does
have certain syntactical constructs to achieve the same end (check the documentation), but you
should avoid this for the purposes of this question.  Think about how you could achieve the
same end given the looping constructs that you know.
*/

(
~transposition = {
	arg noteList, transpositionNumber;
	noteList.do({|item, index|
		if( -1 < (item + transpositionNumber) && (item + transpositionNumber) < 128,
			{noteList[index] = item + transpositionNumber;},
			{noteList = nil});
	});
};
);

// Testing for ~transposition
~transposition.value(List[2, 3], 1).postln; // Should post List[3, 4]
~transposition.value(List[], 23).postln; // Should post List[]
~transposition.value(List[4, 27, 8, 64], 3).postln; // Should post List[7, 30, 11, 67]
a = ~transposition.value(List[0, 67, 2], 123)
a.post;//Should post nil

// Add your own testing here if you like

/*
FUNCTIONAL FUN: Note Mapping

Consider a list of notes in the same format as above.  The function ~numberToNote should
take the list of pitch numbers and return a new list of symbols as letter names where
each symbol is the name of the note represented in the original list.  Remember concert
A is 69.  So a list like List[69, 70] when passed as an argument to ~numberToNote should
return List[A, A#] where A and A# are symbols.

In Western notation, the same pitch can be represented by multiple different names
depending upon context.  For example, A# is the same as Bb.  We call these enharmonic
equivalents.  For this function, use these symbols for the 12 possible notes:
'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'.
*/

(
~numberToNote = {
	arg noteList;
	noteList.do({|item, index|
		if((item%12)==0, {noteList[index] = 'C'},
		{if ((item%12)==1, {noteList[index] = 'C#'},
		{if((item%12)==2, {noteList[index] = 'D'},
		{if((item%12)==3, {noteList[index] = 'D#'},
	    {if((item%12)==4, {noteList[index] = 'E'},
	    {if((item%12)==5, {noteList[index] = 'F'},
	    {if((item%12)==6, {noteList[index] = 'F#'},
		{if((item%12)==7, {noteList[index] = 'G'},
	    {if((item%12)==8, {noteList[index] = 'G#'},
	    {if((item%12)==9, {noteList[index] = 'A'},
	    {if((item%12)==10, {noteList[index] = 'A#'},
	    {if((item%12)==11, {noteList[index] = 'B'})})})})})})})})})})});
	});

};
);})

// Testing for ~numberToNote
~numberToNote.value(List[45, 12]).postln; // Should return List[A, C]
~numberToNote.value(List[61]).postln; // Should return List[C#]
~numberToNote.value(List[]).postln; // Should return List[ ]

// Add your own testing here if you like


/*
FUNCTIONAL FUN: Note Mapping To Key

This exercise is very similar to the previous exercise except that a dictionary is now
used to specify the mapping from note numbers to note symbol.  This allows for a specific
enharmonic spelling, like that of a key signature) based on the dictionary provided.  See
the dictionary example of ~ebMajor below to see the format of the dictionary.
*/
(
~numberToNoteWithKey = {
	arg noteList, keyDict;
	noteList.do({|item, index|
		noteList[index] = keyDict[item%12]
	});
};
);

// Testing for ~numberToNote
(
~ebMajor = Dictionary.newFrom(List[0, 'C', 1, 'C#/Db', 2, 'D', 3, 'Eb', 4, 'E/Fb',
	5, 'F', 6, 'F#/Gb', 7, 'G', 8, 'Ab', 9, 'A/Bbb', 10, 'Bb', 11, 'B/Cb']);
~numberToNoteWithKey.value(List[63, 65, 67, 62, 63, 58, 56, 57, 58], ~ebMajor);
)
// Should return List[ Eb, F, G, D, Eb, Bb, Ab, A/Bbb, Bb ]

// Add your own testing here if you like

/*
FUNCTIONAL FUN: Extract Notes From Song

We can define a song or melody as a series of consecutive notes where each note has
a pitch given as a number and a duration given by a symbol representing Western
notation for rhythm.  For example, \e is an eighth note.  A note, then, is an array
of [<pitch>, <duration>] and a song is an array of notes like [[63, \e], [64, \q]].

The function ~extractvalues should take a song (i.e., an array of arrays) and a
boolean value called noteBool and return a list of either the notes or the
rhythm symbols.   The boolean noteBool determines which list should be returned.
If noteBool is true, then a list of notes should be returned.  If noteBool is false,
then a list of symbols should be returned.  Do NOT construct two lists and choose
the list to be returned at the end.  Only one list should be constructed.
*/

(
~extractValuesFromSong = {
	arg song, noteBool;
	var a = if( noteBool,
		{song.do({|item, index| song[index] = item[0]});},
		{song.do({|item, index| song[index] = item[1]});});
	a

};
);

// Testing for ~extractValuesFromSong
~extractValuesFromSong.value([[63, \e], [62, \e], [61, \q]], true).postln; // Should post List[63, 62, 61]
~extractValuesFromSong.value([[79, \w], [85, \s]], false).postln; // Should post List[w, s]

// Add your own testing here if you like


/*
FUNCTIONAL FUN: Map Duration To Value

All of these functions will be used to play simple songs in the format of an array
of [<pitch>, <duration>].  The function that plays the songs below, ~playSong, only
understands duration as a fractional element of a beat.  For example, a duration of
2 is equivalent to a half note comprising two beats.  We would like to be more flexible
and to name our duration in terms of symbols, such that we could name our durations
anything we like, just as we did in ~extractValuesFromSong.  However, we need some
conversion system to translate between our symbols and a numerical value that
~playSong understands.

The function ~durationToValue accepts an array of durations as symbols and a mapping
dictionary that maps symbols to fractional durations. ~durationToValue should return
a new list of durations where each duration of the old array has been converted to
its numerical equivalent.
*/

(
~durationToValue = {
	arg listOfDurations, mapping;
	var outPut = listOfDurations.do({|item, index| listOfDurations[index] = mapping[item]});
	outPut;
};
);

// Testing for ~durationToValue
~durLettersToNum = Dictionary.newFrom([\w, 4, \h, 2, \q, 1, \e, 0.5, \s, 0.25]);
~durationToValue.value([\w, \e, \s, \s, \q, \q, \h], ~durLettersToNum);
// Should post List[4, 0.5, 0.25, 0.25, 1, 1, 2]

// Add your own testing here if you like

/******************
PLAY YOUR FUNCTIONS
*******************/

// First boot your audio server by either going to the Server tab on the menu and selecting
// "Boot Server" or by executing the following code below

(
s.boot;
)

(
~midiToFreq = {|midiNote| 2**((midiNote - 69)/12) * 440;};

SynthDef(\notePlayer, { |note, dur|
	Out.ar([0, 1],
        SinOsc.ar(note, 0, 0.2) * Line.kr(1, 0, dur, doneAction: Done.freeSelf)
    )
}).add;

~playSong = {
	arg song, transSemitones, keyMapping;
	var noteList = ~transposition.value(~extractValuesFromSong.value(song, true), transSemitones);
	if (noteList == nil, {"Tranposed out of range".postln;}, {
		var noteListLetter = if(keyMapping == nil,
			{~numberToNote.value(noteList)},
			{~numberToNoteWithKey.value(noteList, keyMapping)}
		);
		var durListLetter = ~extractValuesFromSong.value(song, false);
		var durMapping = Dictionary.newFrom([\w, 4, \h, 2, \q, 1, \e, 0.5, \s, 0.25]);
		var durList = ~durationToValue.value(durListLetter, durMapping);
		var index = 0;
		r = Routine{
			while({index < song.size;}, {
				var dur = durList.at(index);
				var note = noteList.at(index);
				var letterNote = noteListLetter.at(index);
				"Note is ".post;
				letterNote.post;
				" | Dur is ".post;
				dur.postln;
				Synth(\notePlayer, [\note, ~midiToFreq.value(note), \dur, dur]);
				index = index + 1;
				dur.wait;
			});
			"Song completed".postln;
		}.play;
	});
};

~odeToJoy = [[63, \e], [63, \e], [64, \e], [66, \e], [66, \e],
	[64, \e], [63, \e], [61, \e], [59, \h]];
~ebMajor = Dictionary.newFrom(List[0, 'C', 1, 'C#/Db', 2, 'D', 3, 'Eb', 4, 'E/Fb', 5,
	'F', 6, 'F#/Gb', 7, 'G', 8, 'Ab', 9, 'A/Bbb', 10, 'Bb', 11, 'B/Cb']);
);

// See how your functions combine to play a song.  Note that you must run all the functions.
~playSong.value(~odeToJoy, 4, ~ebMajor);
~playSong.value(~odeToJoy, 0, nil);

// Compose your own song and play it if you like!






/*
CHALLENGE EXERCISE: Mapping Notes to Frequencies

The letter naming convention of notes in Western music identifies pitch but does not
indicate in which octave a pitch falls.  For example, the note A could be an A on a
flute or an A on a tuba.  To distinguish between the octave of a note, we can use
"scientific pitch notation" which specifies both the note and the octave that the note
is in.  For example, A4 is A in the 4th octave (a.k.a, concert A).  We can also
identify specific notes using their frequency.

Your task is to take a list of notes in scientific pitch notation and convert them to
their frequencies.  Implement the function ~notesToFreqs which accepts two arguments:
1) an array or list of notes in scientific pitch notation, and 2) a mapping dictionary
where the keys are pitches in scientific notation and whose values are frequencies of
those notes in the 0th octave.  You can assume that all of the note names of the note array
in scientific pitch notation can be found in the dictionary.  You can also assume that all
octaves are from 0 to 9.  ~notesToFreqs should return an array (not a list!) of those
frequencies.

To calculate the correct frequency based on the octave, the frequency of the nth octave
is always twice the frequency of the n - 1 frequency.  Frequency is based on powers of
two.  For example, A0 = 27.50Hz; A1 = 27.50 * 2 = 55Hz; A2 = 55 * 2 = 110Hz;
A3 = 110 * 2 = 220Hz; A4 = 220 * 2 = 440Hz; ... etc.

This is an advanced problem and will require to sort through the documentation to think
about the best way to solve this problem.
*/

(
~notesToFreqs = {
	arg arrayOfNotes, mapping;
	var outPut = arrayOfNotes.do({|item, index|
		var aString = item.asString;
		var stringNote = aString.at(0).asString;
		var note = if(aString.contains("#") || aString.contains("b"), {stringNote ++ aString.at(1).asString}, {stringNote});
		var newNote = note.asSymbol;
		var octave = item.asString.at(item.asString.size - 1).asString.asFloat;
		var frequency = mapping[newNote];
		while({octave>0}, {frequency = frequency * 2.00; octave = octave-1});
		arrayOfNotes[index] = frequency.asFloat;
		});
	outPut;
};
);

(
~arrayOfNotes = ['A4', 'C#3', 'Eb7', 'Gb2'];
~mapping = Dictionary.newFrom(List['C', 16.35, 'C#', 17.32, 'Db', 17.32, 'D', 18.35,
	'D#', 19.45, 'Eb', 19.45, 'E', 20.60, 'F', 21.83, 'F#', 23.12, 'Gb', 23.12, 'G', 24.50,
	'G#', 25.96, 'Ab', 25.96, 'A', 27.50, 'A#', 29.14, 'Bb', 29.14, 'B', 30.87]);
)
~notesToFreqs.value(~arrayOfNotes, ~mapping).postln; // Should post [ 440.0, 138.56, 2489.6, 92.48 ]

// Add your own testing here if you like

