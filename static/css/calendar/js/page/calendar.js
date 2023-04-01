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

                // 如果要显示events，就直接在这个list里加就可以了，注意日期格式
                events: [
                    {
                        title: 'flight1',
                        start: '2023-04-1',
                        end: '2023-04-12',
                        id:"demo1"
                    },
                    {
                        title: 'some hotel',
                        start: '2023-04-1',
                        end: '2023-04-3',
                        color: '#009378',
                        id: "demo2"
                    },
                    {
                        title: 'london trip',
                        start: '2023-04-4',
                        end: '2023-04-6',
                        color: '#2bb3c0',
                        id: "demo3"
                    },
                    {
                        title: 'the big ben',
                        start: '2023-04-7',
                        end: '2023-04-8',
                        color: '#e16123',
                        id: "demo4"
                    },
                    {
                        title: 'The Cambridge University',
                        start: '2023-04-9',
                        end: '2023-04-12',
                        color: '#ff4040',
                        id: "demo6"
                    }
                ]

            });
        }
        //删除事件
        // $(document).on('click', '.btn_del', function () {
        //     $calendarApp.fullCalendar('removeEvents');
        //     //下面是删除某个，加载事件的时候添加id
        //     //id可以取数据库里的唯一编号
        //     //$calendarApp.fullCalendar('removeEvents',[id])
        // });
    });
 
    

}(jQuery));
