#pragma once

// Error codes
#define SUCCESS_CODE  0
#define WARNINGS_CODE 1
#define ERRORS_CODE   2
#define CRUSH_CODE    3

// Token types
#define NONE 	  {0}
#define NAME 	  {1}
#define COLON 	{2}
#define EQUAL 	{3}
#define INT 	  {4}
#define NE 	    {5}
#define ARL 	  {6}
#define CUL 	  {7}
#define BUX 	  {8}
#define PAL 	  {9}
#define PAR 	  {10}
#define STRING  {11}
#define CUR 	  {12}
#define GT 	    {13}
#define LT  	  {14}
#define GE 	    {15}
#define LE 	    {16}
#define ARR 	  {17}
#define SHL 	  {18}
#define SHR 	  {19}
#define BLL 	  {20}
#define BLR 	  {21}
#define PLUS 	  {22}
#define MINUS   {23}
#define MULT 	  {24}
#define DIV 	  {25}
#define POW 	  {26}
#define IDIV 	  {27}
#define MOD 	  {28}
#define OR 	    {29}
#define AND 	  {30}
#define XOR 	  {31}
#define NOT 	  {32}
#define NEG 	  {33}
#define BINNEG      {34}
#define RESERVED 	  {35}
#define ARRAYTYPE   {36}
#define SO 	        {37}
#define ASSIGN 	    {38}
#define MINUSASSIGN {39}
#define PLUSASSIGN 	{40}
#define INC 	      {41}
#define DEC 	      {42}
#define NEGASSIGN 	{43}
#define SYSTAG 	    {44}
#define POWASSIGN   {45}
#define POW 	      {46}
#define MULASSIGN 	{47}
#define MUL 	      {48}
#define IDIVASSIGN 	{49}
#define DIVASSIGN 	{50}
#define MODAPPLY 	  {51}
#define MODASSIGN 	{52}
#define BOOLOR 	    {53}
#define ORASSIGN 	  {54}
#define BOOLXOR 	  {55}
#define XORASSIGN   {56}
#define BOOLAND 	  {57}
#define ANDASSIGN   {58}
#define COMMA 	    {59}
#define DOT 	      {60}
#define RANGE 	    {61}
#define ELLIPSE 	  {62}


// Parser consts
#define ROOT 	 {63}
#define CLASS 	 {64}
#define CLASS_NAME 	 {65}
#define CLASS_BODY_OR_SUPER 	 {66}
#define CLASS_SUPER 	 {67}
#define CLASS_BODY 	 {68}
#define CLASS_OPEN_BODY 	 {69}
#define FN 	 {70}
#define FN_NAME 	 {71}
#define FN_OPEN_ARGS 	 {72}
#define FN_ARG_NAME_OR_ARGS_CLOSE 	 {73}
#define FN_ARG_COLON 	 {74}
#define FN_ARG_TYPE 	 {75}
#define FN_ARG_COMMA_OR_ARRAY_OR_CLOSE 	 {76}
#define FN_ARG_INT_OR_CLOSE_ARRAY 	 {77}
#define FN_ARG_COMMA_OR_CLOSE 	 {78}
#define FN_BODY_OPEN_OR_ARR 	 {79}
#define FN_ARG_CLOSE_ARRAY 	 {80}
#define FN_BODY 	 {81}
#define FN_RTYPE 	 {82}
#define FN_OPEN_BODY 	 {83}
#define IF_COND 	 {84}
#define FREE_NAME 	 {85}
#define UNLINK_NAME 	 {86}
#define RETURN_VALUE 	 {87}
#define WHILE_VALUE 	 {88}
#define CALL_OR_DEFINE_OR_ASSIGN 	 {89}
#define DEFINITION 	 {90}
#define CALL 	 {91}
#define CALL_ARGS 	 {92}
#define FN_BEGIN 	 {93}
#define CALL_COMMA_OR_CLOSE 	 {94}
#define EXPR 	 {95}
#define EXPR_OP 	 {96}
#define EXPR_CALL_OR_OP 	 {97}
#define CALL_END 	 {98}

// Stack consts
#define LITERAL 	 {99}

// System data
#define VERSION  "0.1.3a"
#define REVISION "r0072"
#define STD "HEP0"

# Help page
char* HELP = "Honey {VERSION} {REVISION} {STD} help page\
\
Usage: hny [options] file...\
\
Options:\
\t--help:  \tShows this page\
\t--debug: \tDeveloper option, enables debug mode in compiler. Not for regular use\
\t--fasm:  \tOutput is FASM code\
\t--hasm:  \tOutput is middle-language production\
\t-Wextra: \tEnables unnecessary warnings\
\t-Werror: \tHandles warnings as errors\
\t-Wno-|w|:\tDisables given warning, for instanse option \"-Wno-unkseq\" will\
\t         \tdisable warning about unknown escape sequences
";

// Lexer constants
#define ALPHA "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
#define DIGIT "0123456789"
#define ALNUM "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
#define SPACE " \b\r\a\v\n\t"

// More system consts
// KNOWN_WARNINGS: dict = {
//     "unkseq": "Unknown sequense warning",
// }
