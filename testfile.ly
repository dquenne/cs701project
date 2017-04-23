%{
Welcome to LilyPond
===================

Congratulations, LilyPond has been installed successfully.

Now to take it for the first test run.

  1. Save this file

  2. Select

       Compile > Typeset file

  from the menu.

  The file is processed, and

  3.  The PDF viewer will pop up. Click one of the noteheads.


That's it.  For more information, visit http://lilypond.org .

%}

\header{
  title = "A scale in LilyPond"
}

\relative c' {
	\clef "alto"
  c d e f f f b c
}

\relative c'' {
	\clef "alto"
 c b b, cis b c8 << { a8 g'4.( a4.) } \\ { g,4. b8 a4. } >>
}


\version "2.18.2"  % necessary for upgrading to future LilyPond versions.
