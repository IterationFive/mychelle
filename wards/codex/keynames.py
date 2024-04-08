'''

This file is not in any way copyrighted.  

This file contains a map of key ids (as returned by curses' 
window.getch()) to friendlier names.  

This map was generated under windows 10, running python at
the command prompt, with the optimistic assumption that these 
values will be the same acoss platform.

A few notes:

This map was generated under windows 10, running python at
the command prompt, with the optimistic assumption that these 
values will be the same acoss platform.

F11 should return 275.  It doesn't.  It returns 546.  Also, 
it toggles fullscreen mode. alt+Enter and alt+padenter 
do the same (with the same 546).  

Certain keys do not register as a keystroke, as a 
limitation of either windows or curses.  In some case, 
windows or another application will take over.
(In the case of Shift+Ins and Ctrl+v, they paste the 
contents of the keyboard.)

These keys might be available in other environments.  

ctrl+escape
alt+escape
shift+backspace
shift+escape
alt+f1
alt+f2
alt+f3
alt+f4
alt+f5
alt+f6
alt+f7
alt+f8
alt+f9
alt+f10
alt+f11
alt+f12
ctrl+a
ctrl+c
ctrl+f
ctrl+h
ctrl+m
ctrl+v
alt+z
ctrl+home
ctrl+end
ctrl+up
ctrl+down
ctrl+padhome
ctrl+padend
ctrl+padup
ctrl+paddown
shift+insert
shift+delete
shift+home
shift+end
shift+pageup
shift+pagedown
shift+up
shift+down
shift+left
shift+right
shift+padinsert
shift+padhome
shift+padend
shift+padpageup
shift+padpagedown
shift+padup
shift+paddown
shift+padleft
shift+padright


Certain keys produce an identical response to other keys:

ctrl+h* backspace
ctrl+i* : tab
ctrl+j* : enter
shift+enter :  enter
alt+enter* : f11**
alt+padenter : f11**
ctrl+[ : escape 

*these items have been commented out on the map  
**F11 as it appears in this map, value 546.

Certain keys, for reasons lost to God, history, and the 
acoustic modem, return 0.  These are as follows:

ctrl+1
ctrl+2
ctrl+3
ctrl+4
ctrl+5
ctrl+6
ctrl+7
ctrl+8
ctrl+9
ctrl+0
ctrl+`
ctrl+-
ctrl+=
ctrl+]
ctrl+,
ctrl+.
ctrl+/
alt+`
alt+-
alt+=
alt+[
alt+]
alt+\
alt+'
alt+,
alt+.
alt+/


It should be noted that certain keystrokes are listed because their
order in the sequence was obvious, but are still unavailable, as per above.
'''

KEYS={
8 : 'backspace',
9 : 'tab',
10 : 'enter',
27 :'escape',
127 : 'ctrl+backspace',
504 : 'alt+backspace',
351 :'shift+tab' ,
482: 'ctrl+tab' ,
265 : 'f1',
266 : 'f2',
267 : 'f3',
268 : 'f4',
269 : 'f5',
270 : 'f6',
271 : 'f7',
272 : 'f8',
273 : 'f9',
274 : 'f10',
546 : 'f11',
276 : 'f12',
289 : 'ctrl+f1',
290 : 'ctrl+f2',
291 : 'ctrl+f3',
292 : 'ctrl+f4',
293 : 'ctrl+f5',
294 : 'ctrl+f6',
295 : 'ctrl+f7',
296 : 'ctrl+f8',
297 : 'ctrl+f9',
298 : 'ctrl+f10',
# 299 : 'ctrl+f11',
300 : 'ctrl+f12',
277 : 'shift+f1',
278 : 'shift+f2',
279 : 'shift+f3',
280 : 'shift+f4',
281 : 'shift+f5',
282 : 'shift+f6',
283 : 'shift+f7',
284 : 'shift+f8',
285 : 'shift+f9',
286 : 'shift+f10',
287 : 'shift+f11',
288 : 'shift+f12',
1 : 'ctrl+a',
2 : 'ctrl+b',
3 : 'ctrl+c',
4 : 'ctrl+d',
5 : 'ctrl+e',
7 : 'ctrl+g',
# 8 : 'ctrl+h',
# 9 : 'ctrl+i',
# 10 : 'ctrl+j',
11 : 'ctrl+k',
12 : 'ctrl+l',
13 : 'ctrl+m',
14 : 'ctrl+n',
15 : 'ctrl+o',
16 : 'ctrl+p',
17 : 'ctrl+q',
18 : 'ctrl+r',
19 : 'ctrl+s',
20 : 'ctrl+t',
21 : 'ctrl+u',
22 : 'ctrl+v',
23 : 'ctrl+w',
24 : 'ctrl+x',
25 : 'ctrl+y',
26 : 'ctrl+z',
417 : 'alt+a',
418 : 'alt+b',
419 : 'alt+c',
420 : 'alt+d',
421 : 'alt+e',
422 : 'alt+f',
423 : 'alt+g',
424 : 'alt+h',
425 : 'alt+i',
426 : 'alt+j',
427 : 'alt+k',
428 : 'alt+l',
429 : 'alt+m',
430 : 'alt+n',
431 : 'alt+o',
432 : 'alt+p',
433 : 'alt+q',
435 : 'alt+r',
436 : 'alt+s',
437 : 'alt+t',
438 : 'alt+u',
439 : 'alt+v',
440 : 'alt+w',
441 : 'alt+x',
442 : 'alt+y',
443 : 'alt+z',
331 : 'insert',
330 : 'delete',
262 : 'home',
358 : 'end',
339 : 'pageup',
338 : 'pagedown',
259 : 'up',
258 : 'down',
260 : 'left',
261 : 'right',
459 : 'padenter',
506 : 'padinsert',
462 : 'paddelete',
449 : 'padhome',
455 : 'padend',
458 : 'padslash',
463 : 'padasterisk',
464 : 'padminus',
465 : 'padplus',
451 : 'padpageup',
457 : 'padpagedown',
450 : 'padup',
456 : 'paddown',
452 : 'padleft',
454 : 'padright',
453 : 'padcenter',
529 : 'ctrl+enter',
477 : 'ctrl+insert',
527 : 'ctrl+delete',
445 : 'ctrl+pageup',
446 : 'ctrl+pagedown',
443 : 'ctrl+left',
444 : 'ctrl+right',
460 : 'ctrl+padenter',
507 : 'ctrl+padinsert',
466 : 'ctrl+paddelete',
516 : 'ctrl+padpageup',
510 : 'ctrl+padpagedown',
511 : 'ctrl+padleft',
513 : 'ctrl+padright',
470 : 'ctrl+padslash',
471 : 'ctrl+padasterisk',
469 : 'ctrl+padminus',
468 : 'ctrl+padplus',
512 : 'ctrl+padcenter',
546 : 'alt+enter',
479 : 'alt+insert',
478 : 'alt+delete',
486 : 'alt+home',
489 : 'alt+end',
487 : 'alt+pageup',
488 : 'alt+pagedown',
490 : 'alt+up',
491 : 'alt+down',
493 : 'alt+left',
492 : 'alt+right',
517 : 'alt+padinsert',
476 : 'alt+paddelete',
524 : 'alt+padhome',
518 : 'alt+padend',
526 : 'alt+padpageup',
520 : 'alt+padpagedown',
525 : 'alt+padup',
519 : 'alt+paddown',
521 : 'alt+padleft',
523 : 'alt+padright',
474 : 'alt+padslash',
530 : 'shift+padenter',
531 : 'shift+padasterisk',
532 : 'shift+padminus',
534 : 'shift+padplus',
533 : 'shift+padcenter',
28 : 'ctrl+\\',
39 : 'ctrl+:',
461 : 'ctrl+\'',
408 : 'alt+1',
409 : 'alt+2',
410 : 'alt+3',
411 : 'alt+4',
412 : 'alt+5',
413 : 'alt+6',
414 : 'alt+7',
415 : 'alt+8',
416 : 'alt+9',
407 : 'alt+0',
500 : 'alt+:'
}

PADTRANSLATION = {
    459:10,
    449:262,
    455:358,
    506:331,
    462:330,
    451:339,
    457:338,
    450:259,
    456:258,
    452:260,
    454:261,
    507:477,
    466:527,
    516:445,
    510:446,
    511:443,
    513:444,
    524:486,
    518:489,
    517:479,
    476:478,
    526:487,
    520:488,
    525:490,
    519:491,
    521:493,
    523:492,
    463:42,
    458:47,
    464:45,
    465:43}