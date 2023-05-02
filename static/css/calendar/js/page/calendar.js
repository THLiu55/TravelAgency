/*

Project     : DAdmin - Responsive Bootstrap HTML Admin Dashboard
Version     : 1.1
Author      : ThemeLooks
Author URI  : http://www.bootstrapmb.com/item/2664

*/

(function ($) {
    "use strict";

    /* ------------------------------------------------------------------------- *
     * COMMON VARIABLES
     * ------------------------------------------------------------------------- */
    var $wn = $(window),
        $document = $(document),
        $body = $('body');

    $(function () {
        var retrieved_events
        $.ajax({
              url: '../plan_events',
              method: 'GET', // 可以是 GET 或 POST
              dataType: 'json', // 返回的数据类型
              success: function(data) {
                // 成功获取数据后的处理
                console.log(data);
                retrieved_events = data;
                // replace events list with retrieved data
                $calendarApp.fullCalendar('removeEvents');
                $calendarApp.fullCalendar('addEventSource', retrieved_events);
              },
              error: function(xhr, status, error) {
                // 获取数据失败后的处理
                console.log("Error: " + error);
              }
        });

        /* ------------------------------------------------------------------------- *
         * CALENDAR EVENTS
         * ------------------------------------------------------------------------- */
        var $calendarEvents = $('.calendar--events'),
            $calendarEventsEl = $calendarEvents.children('.fc-events'),
            $calendarEventEl = $calendarEventsEl.children('.fc-event'),
            $calendarEventsInput = $calendarEvents.find('.form-check-input');

        if ( $calendarEvents.length ) {
            $calendarEventEl.each(function () {
                var $el = $(this),
                    bgColor = $el.css('background-color');

                $el.draggable({
                        revert: true,
                        revertDuration: 0,
                        zIndex: 999
                    })
                    .css({
                        'border-color': bgColor
                    })
                    .data('event', {
                        title: $el.text(),
                        color: bgColor,
                        stick: true
                    });
            });
        }

        $calendarEvents.on('click', '.calendar--event__colors li', function () {
            var $el = $(this);

            $el.addClass('active').siblings().removeClass('active');
        });

        $calendarEvents.on('submit', 'form', function (e) {
            e.preventDefault();

            var $el = $(this),
                $input = $el.children('input'),
                $event = $('<div></div>'),
                $colorClass = $calendarEvents.find('.calendar--event__colors .active'),
                $bdColor = $colorClass.css('background-color');

            $event.draggable({
                    revert: true,
                    revertDuration: 0,
                    zIndex: 999
                })
                .css({
                    'border-color': $bdColor
                })
                .data('event', {
                    title: $input.val(),
                    color: $bdColor,
                    stick: true
                })
                .addClass( ' fc-event ' + $colorClass.attr('class') )
                .text( $input.val() )
                .appendTo($calendarEventsEl);

        });

        /* ------------------------------------------------------------------------- *
         * CALENDAR APP
         * ------------------------------------------------------------------------- */
        var $calendarApp = $('#calendarApp');

        if ( $calendarApp.length ) {
            $calendarApp.fullCalendar({
                header: {
                    left: '',
                    center: 'prev next title',
                    right: 'today basicDay basicWeek month'
                },
                // locale:'zh-cn',
                editable: true,
                droppable: true,
                drop: function () {
                    if ( $calendarEventsInput.is(':checked') ) {
                        $(this).remove();
                    }
                },
                timeFormat: 'h(:mm)a',
                events: retrieved_events

            });
        }
        // 删除事件
        $(document).on('click', '.btn_del', function () {
            $calendarApp.fullCalendar('removeEvents');
            //下面是删除某个，加载事件的时候添加id
            //id可以取数据库里的唯一编号
            //$calendarApp.fullCalendar('removeEvents',[id])
        });
    });
 
    

}(jQuery));
