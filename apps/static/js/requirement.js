/**
 * Created by zhaoliang on 15/12/19.
 */
(function() {
    var STRING_DECAMELIZE_REGEXP = (/([a-z\d])([A-Z])/g);
    var STRING_STRIP_HTML_REGEXP = (/(<[^>]*>)/g);
    var STRING_DASHERIZE_REGEXP  = (/[^a-z\d]+/g);

    var decamelize = function(str) {
        return str.replace(STRING_DECAMELIZE_REGEXP, '$1_$2').toLowerCase();
    };

    var stripHtml = function(str) {
        return str.replace(STRING_STRIP_HTML_REGEXP, '');
    };

    var headings = [];

    $('h3, h4').each(function(index, heading) {
        var textContent = heading.textContent;

        var value = {
            el: headings,
            id: heading.id,
            text: textContent,
            children: []
        };

        if (heading.tagName.toUpperCase() === 'H3') {
            headings.push(value);
            current = value;
        } else {
            current.children.push(value);
        }
    });

    function renderHeadings(headings) {
        var template = '';
        var obj = headings[0];
        $.each(headings, function(i, heading) {
            template += '<li><a href="#' + heading.id + '">' + heading.text + '</a>';

            if (heading.children.length) {
                template += '<ul class="nav">';
                template += renderHeadings(heading.children);
                template += '</ul>';
            }

            navContent += '</li>';
        });

        return template;
    }

    var navContent = renderHeadings(headings);

    var $sidebar = $('.sidebar');

    $sidebar.find('.nav').html(navContent);

    $sidebar.affix({
        offset: {
            top: function() {
                //var offsetTop = $sidebar.offset().top;
                //var navbarOuterHeight = $('.navbar').height();
                //var sidebarMargin = parseInt($sidebar.children(0).css('margin-top'), 10);
                //console.log('+++'+offsetTop+'+++'+navbarOuterHeight+'+++'+sidebarMargin+'+++'+(offsetTop - navbarOuterHeight - sidebarMargin));
                //return offsetTop - navbarOuterHeight - sidebarMargin;
                return 100;
            },
            bottom: function() {
                return $('.footer').outerHeight(true);
            }
        }
    });

    var $body = $(document.body);

    $body.scrollspy({
        target: '.sidebar',
        offset: 140
    });

}());