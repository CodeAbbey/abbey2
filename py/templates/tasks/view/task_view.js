function LanguageDetector() {
    function countCharacters(s) {
        var cnt = [];
        for (var i = 0; i < 256; i++) {
            cnt[i] = 0;
        }
        for (var j = 0; j < s.length; j++) {
            var c = s.charCodeAt(j);
            if (c >= 0 && c < 256) {
                cnt[i]++;
            }
        }
        return cnt;
    }

    this.detect = function(s) {
        var cnt = countCharacters(s);
        var len = s.length;
        var lenBf = s.replace(/[^\+\-\.\,\[\]\<\>\:\;\s]/g, '').length;
        if (lenBf / (len + 1) > 0.6 && s.indexOf('#include') < 0) {
            return 'bf';
        }
        if (s.indexOf('var ') >= 0) {
            return s.indexOf('using ') >= 0 ? 'cs' : 'js';
        }
        if (/\bdef\b/.test(s) && /\bend\b/.test(s)) {
            return 'ruby';
        }
        if (/with\s+ada/i.test(s)) {
            return 'ada';
        }
        if (/fn\s+main/.test(s)) {
            return 'rust';
        }
        var endLines = s.match(/[\,\;\{\}][\040\t]*[\n\r]/);
        endLines = endLines !== null ? endLines.length : 0;
        if (endLines / (cnt[10] + 1) > 0.4) {
            if (s.indexOf('#include') >= 0) {
                return 'cpp';
            }
            if (/main\s*\(\s*String/.test(s)) {
                return 'java';
            }
            if (cnt['$'.charCodeAt(0)] / len > 0.005) {
                return 'php';
            }
            return 'cs';
        } else {
            if (/\([\+\*]/.test(s)) {
                return 'lisp';
            }
            if (s.indexOf('dim ') >= 0) {
                return 'basic';
            }
            if (s.indexOf('local ') >= 0) {
                return 'lua';
            }
            return 'py';
        }
    }
}

var languageDetector = new LanguageDetector();

function findLanguageName(key) {
    return $('#language-select option[value=' + key + ']').text();
}

function beforeSolutionSubmit() {
    var solTextArea = $('#solution');
    if (solTextArea.length == 0) {
        return true;
    }
    var text = solTextArea.val();
    var detected = languageDetector.detect(text);
    var selected = $('#language-select').val();
    if (detected != selected) {
        return confirm('Are you sure your solution is in "'
            + findLanguageName(selected) + '" language?\n\n'
            + 'If not, click "Cancel" and choose proper language please...\n'
            + '(perhaps, "' + findLanguageName(detected) + '"?)');
    }
}

function reloadSolution(lang) {
    window.aceEditor.setValue(atob(window.storedSolutions[lang]));
    window.aceEditor.getSelection().selectFileStart();
    $('#language-select').val(lang).change();
}

function reloadSolutionLink(lang) {
    reloadSolution(lang);
    $('#load-solution-modal').modal('hide');
}

function changeEditorLanguage() {
    var lang = $('#language-select').val();
    switch (lang) {
        case "cpp": lang = "c_cpp";break;
        case "cs": lang = "csharp";break;
        case "java": lang = "java";break;
        case "js": lang = "javascript";break;
        case "py": lang = "python";break;
        case "ruby": lang = "ruby";break;
        case "scala": lang = "scala";break;
        default: lang = "plain_text";break;
    }
    aceEditor.getSession().setMode("ace/mode/" + lang);
}

function executeCode() {
    var data = {
        code: btoa($('#solution').val()),
        input: btoa($('#inputdata').val()),
        lang: $('#language-select').val(),
    };
    var runButton = $('#run-code');
    runButton.attr('disabled', 'true');
    var answerField = $('#answer');
    answerField.focus();
    answerField.val('please wait please wait ');
    var timer = setInterval(function(){
        var s = answerField.val();
        answerField.val(s.substring(1) + s[0]);
    }, 117);
    $.ajax({
        type: 'POST',
        url: "{{url_for('tools.run_code')}}",
        data: JSON.stringify(data),
        contentType: 'application/json',
        dataType: 'text',
        success: function(res) {
            clearInterval(timer);
            answerField.val(res);
            runButton.attr('disabled', null);
        }
    });
}

$(function() {
    $('#run-code').click(executeCode);
    var solutionTextarea = $('#solution');
    if (solutionTextarea.length > 0) {
        solutionTextarea.hide();
        window.aceEditor = ace.edit('solution-div', {
            minLines: 10,
            maxLines: 30,
            showPrintMargin: false,
            fontSize: '1rem',
            mode: 'ace/mode/plain_text',
        });
        window.aceEditor.getSession().on('change', function() {
            solutionTextarea.val(window.aceEditor.getSession().getValue());
        });
        $('#language-select').change(changeEditorLanguage);
        $.get("{{url_for('tasks.get_solution', taskid=data['id'])}}", function(data) {
            window.storedSolutions = data;
            var keys = Object.keys(data);
            var solLinksBody = $('#solution-links');
            for (var i in keys) {
                $('<a></a>').attr('href', '#').attr('onclick', 'reloadSolutionLink("' + keys[i] + '")')
                    .text(findLanguageName(keys[i])).appendTo(solLinksBody);
                solLinksBody.append(' ');
            }
            if (keys.length > 0) {
                var lang = keys[0];
                reloadSolution(lang);
            }
        });
    }
});


