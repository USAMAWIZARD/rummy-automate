
function Hand(cards, jokers, round, wilds) {
    this.cards = clone(cards);
    this.jokers = jokers;
    this.wilds = wilds || 0;
    this.round = round;
    this.melds = [];
    this.value = this.leftoverValue();
}

// FIND MELDS FROM CURRENT POINT

Hand.prototype.findMelds = function(suit, number) {

    // IF NOT A RECURSION: CONVERT WILDCARDS TO JOKERS AND START FROM 0,0
    if (suit == undefined || number == undefined) {
        suit = number = 0;
        var noRecursion = true;
        this.convertWilds();
    }

    // FIND CARDS FROM CURRENT POINT UNTIL END OR FULL LAY-DOWN
    while (suit < 5 && this.value > 0) {
        if (this.cards[suit][number] > 0) {

            // FIND RUNS STARTING WITH CURRENT CARD
            var run = this.findRun(suit, number);

            // TRY DIFFERENT LENGTHS OF LONG RUN
            for (var len = 3; len <= run.length; len++) {

                // SKIP LONG RUNS ENDING WITH A JOKER
                if (len > 3 && run[len - 1].s == -1) continue;

                // CREATE COPY OF HAND, REMOVE RUN AND START RECURSION
                var test = new Hand(this.cards, this.jokers, this.round, this.wilds);
                test.removeCards(run.slice(0, len));
                test.findMelds(suit, number);

                // SAVE CURRENT RUN AND MELDS FOUND THROUGH RECURSION IF BETTER VALUE IS FOUND
                if (test.value < this.value) {
                    this.value = test.value;
                    this.melds.length = 0;
                    this.melds = [].concat(run.slice(0, len), test.melds);
                }
            }
        }

        // MOVE THROUGH CARD MATRIX
        if (++number > 10) {
            number = 0;
            ++suit;
        }
    }

    // AFTER ALL CARDS HAVE BEEN CHECKED FOR RUNS, CREATE COPY OF HAND AND FIND SETS
    if (this.value > 0) {
        var test = new Hand(this.cards, this.jokers, this.round, this.wilds);
        test.findSets();

        // SAVE SETS IF BETTER VALUE IS FOUND
        if (test.value < this.value) {
            this.value = test.value;
            this.melds.length = 0;
            while (test.melds.length) this.melds.push(test.melds.shift());
        }
    }

    // FIX NO MELDS AND ONE JOKER EXCEPTION
    if (noRecursion && this.melds.length < 3) {
        this.melds.length = 0;
        this.value = this.leftoverValue();
    }
}

// FIND RUN STARTING WITH CURRENT CARD

Hand.prototype.findRun = function(s, n) {
    var run = [], jokers = this.jokers;
    while (n < 11) {
        if (this.cards[s][n] > 0) {
            run.push({s:s, n:n});
        } else if (jokers > 0) {
            run.push({s:-1, n:-1});
            jokers--;
        } else break;
        n++;
    }

    // ADD LEADING JOKERS (AT END FOR CODE SIMPLICITY)
    while (run.length < 3 && jokers--) {
        run.push({s:-1, n:-1});
    }

    // REMOVE UNNECESSARY TRAILING JOKERS
    while (run.length > 3 && run[run.length - 1].s == -1) {
        run.pop();
    }
    return run;
}

// FIND SETS

Hand.prototype.findSets = function() {
    var sets = [[], []], values = [[], []];
    for (var n = 0; n < 11; n++) {
        var set = [], value = 0;
        for (var s = 0; s < 5; s++) {
            for (var i = 0; i < this.cards[s][n]; i++) {
                set.push({s:s, n:n});
                value += n + 3;
            }
        }

        // ADD COMPLETE SET TO MELDS, OR INCOMPLETE SET TO CANDIDATES TO RECEIVE JOKERS
        if (set.length >= 3) {
            this.addToMelds(set);
        }
        else if (set.length > 0) {
            // STORE ONE-CARD SETS IN sets[0] AND TWO-CARD SETS IN sets[1]
            sets[set.length - 1].push(set);
            values[set.length - 1].push(value);
        }
    }

    // IF TWO JOKERS ARE AVAILABLE: COMPLETE MOST VALUABLE TWO-CARD SET OR ONE-CARD SET(S)
    while (this.jokers > 1 && sets[0].length > 0) {
        var select = values[0][sets[0].length - 1];
        for (var i = sets[1].length - 1; i >= 0 && i > sets[1].length - 3; i--) {
            select -= values[1][i];
        }
        if (select > 0) {
            set = sets[0].pop(); values[0].pop();
            set.push({s:-1, n:-1}, {s:-1, n:-1});
            this.addToMelds(set);
        } else {
            for (var i = 0; i < 2 && sets[1].length > 0; i++) {
                set = sets[1].pop(); values[1].pop();
                set.push({s:-1, n:-1});
                this.addToMelds(set);
            }
        }
    }

    // IF JOKER IS AVAILABLE: COMPLETE MOST VALUABLE TWO-CARD SET
    while (this.jokers > 0 && sets[1].length > 0) {
        set = sets[1].pop();
        set.push({s:-1, n:-1});
        this.addToMelds(set);
    }

    // ADD LEFT-OVER JOKERS
    while (this.jokers > 0) {
        this.addToMelds([{s:-1, n:-1}]);
    }
}

// ADD SET TO MELDS

Hand.prototype.addToMelds = function(set) {
    this.removeCards(set);
while (set.length) this.melds.push(set.shift());
}

// REMOVE ARRAY OF CARDS FROM HAND

Hand.prototype.removeCards = function(cards) {
    for (var i = 0; i < cards.length; i++) {
        if (cards[i].s >= 0) {
            this.cards[cards[i].s][cards[i].n]--;
        } else this.jokers--;
    }
    this.value = this.leftoverValue();
}

// GET VALUE OF LEFTOVER CARDS

Hand.prototype.leftoverValue = function() {
    var leftover = 0;
    for (var i = 0; i < 5; i++) {
        for (var j = 0; j < 11; j++) {
            leftover += this.cards[i][j] * (j + 3) // cards count from 0 vs 3
        }
    }
    return leftover + 25 * this.jokers - (22 - round) * (this.jokers < this.wilds ? this.jokers : this.wilds);
}

// CONVERT WILDCARDS TO JOKERS

Hand.prototype.convertWilds = function() {
    for (var i = 0; i < 5; i++) {
        while (this.cards[i][this.round] > 0) {
	this.cards[i][this.round]--;
            this.jokers++; this.wilds++;
        }
    }
    this.value = this.leftoverValue();
}

// UTILS: 2D ARRAY DEEP-COPIER

function clone(a) {
    var b = [];
    for (var i = 0; i < a.length; i++) {
        b[i] = a[i].slice();
    }
    return b;
}

// UTILS: SHOW HAND IN CONSOLE

function showHand(c, j, r, v) {
    var num = "    3 4 5 6 7 8 9 T J Q K";
    console.log(num.slice(0, 2*r+4) + "w" + num.slice(2*r+5));
    for (var i = 0; i < 5; i++) {
        console.log(["CLB ","DMD ","HRT ","SPD ","STR "][i] + c[i]);
    }
    console.log("    jokers: " + j + "  value: " + v);
}

// UTILS: SHOW RESULT IN CONSOLE

function showResult(m, v) {
    if (m.length == 0) console.log("no melds found");
    while (m.length) {
        var c = m.shift();
        if (c.s == -1) console.log("joker *");
        else console.log(["clubs","dmnds","heart","spade","stars"][c.s] + " " + "3456789TJQK".charAt(c.n));
    }
    console.log("leftover value: " + v);
}

// TEST DATA: CREATE ARRAY OF ALL CARDS TO DRAW FROM

var pack = [{s:-1,n:-1},{s:-1,n:-1},{s:-1,n:-1},{s:-1,n:-1},{s:-1,n:-1},{s:-1,n:-1}];
for (var i = 0; i < 5 ; i++) {
    for (var j = 0; j < 11; j++) {
        pack.push({s:i, n:j}, {s:i, n:j});
    }
}

// TEST DATA: CREATE 2D ARRAY TO STORE CARDS

var matrix = [];
for (var i = 0; i < 5; i++) {
    matrix[i] = [];
    for (var j = 0; j < 11; j++) {
        matrix[i][j] = 0;
    }
}

// TEST DATA: DRAW CARDS AND FILL 2D ARRAY

var round = 10; // count from zero
var jokers = 0;
for (i = 0; i < round + 3; i++)
{
    var j = Math.floor(Math.random() * pack.length);
    var pick = pack[j];
    pack[j] = pack.pop();
    if (pick.s > -1) matrix[pick.s][pick.n]++;
    else jokers++;
}

// USE THIS TO TEST SPECIFIC HANDS

// round = 10; // count from zero
// matrix = [[0,0,0,0,0,1,0,0,0,0,1],
//           [0,0,0,0,0,1,0,0,0,0,0],
//           [0,1,0,0,1,2,0,0,0,0,0],
//           [0,0,0,0,0,2,1,0,0,1,1],
//           [0,0,0,0,0,0,0,0,0,0,0]];
// jokers = 1;

// CREATE INSTANCE OF HAND OBJECT, EVALUATE AND SHOW RESULT


var x = new Hand(matrix, jokers, round); // CALL WITHOUT FOURTH (WILDS) PARAMETER
showHand(x.cards, x.jokers, x.round, x.value);
x.findMelds();                           // CALL WITHOUT PARAMETERS TO INITIATE EVALUATION
showResult(x.melds, x.value);