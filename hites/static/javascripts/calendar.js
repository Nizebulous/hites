MONTHS = [
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC"
];
DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
];

TODAY = new Date();
YEAR = TODAY.getFullYear();
MONTH = TODAY.getMonth();
DIV = document.getElementById('cal-table');
ANCHOR = new Date(2014, 8, 3);

function getMonthInfo(year, month) {
    var url = window.location.protocol + "//" + window.location.host + "/woodworking/" + year + "/" + month + "/events";
    var representationOfDesiredState = "The cheese is old and moldy, where is the bathroom?";
    var client = new XMLHttpRequest();
    client.open("GET", url, false);
    client.send(null);
    if (client.status != 200)
        alert("The request did not succeed!\n\nThe response status was: " + client.status + " " + client.statusText + ".");
    return JSON.parse(client.responseText);
}

function weekDiff(date1, date2) {
	// The number of milliseconds in one week
    var msWeek = 604800000;

    var diff = Math.abs(date1.getTime() - date2.getTime());
	return Math.floor(diff / msWeek);
}

function mod(m, n) {
        return ((m % n) + n) % n;
}

function navYear(years) {
    YEAR = YEAR + years;
    renderCalendar(DIV);
}

function navMonth(months) {
    MONTH = MONTH + months;
    YEAR = YEAR + Math.floor(MONTH / MONTHS.length);
    MONTH = mod(MONTH, MONTHS.length);
    renderCalendar(DIV);
}

function createNav(display_text, navFunc) {
    var link = document.createElement('A');
    link.innerHTML = display_text;
    link.href = 'javascript:'+navFunc;
    return link;
}

function createNavRow(display_text, navFunc) {
    var row = document.createElement('TR');
    var left = row.insertCell();
    left.appendChild(createNav('<<', navFunc+'(-1)'));
    var center = row.insertCell();
    center.innerHTML = display_text;
    center.align = 'center';
    center.style.width = 100;
    var right = row.insertCell();
    right.appendChild(createNav('>>', navFunc+'(1)'));
    return row;
}

function renderCalendar(div) {
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
    var headerTable = document.createElement('TABLE');
    headerTable.align = 'center';
    headerTable.appendChild(createNavRow(YEAR, 'navYear'));
    headerTable.appendChild(createNavRow(MONTHS[MONTH], 'navMonth'));

    date_info = getMonthInfo(YEAR, MONTH + 1);

    var table = document.createElement('TABLE');
    table.align = 'center';
    // Days of the week
    var dayRow = table.insertRow();
    for (i = 0; i < DAYS.length; i++) {
        var cell = dayRow.insertCell();
        cell.setAttribute('class', 'cal-weekday')
        cell.style.width = 100;
        cell.innerHTML = DAYS[i];
    }
    var firstDayOfMonth = new Date(YEAR, MONTH, 1);
    var lastDayOfMonth = new Date(YEAR, MONTH + 1, 0);
    var indexDate = new Date(YEAR, MONTH, firstDayOfMonth.getDate() - firstDayOfMonth.getDay());
    while (indexDate <= lastDayOfMonth) {
        var row = table.insertRow()
        for (i = 0; i < DAYS.length; i++) {
            var cell = row.insertCell();
            var date = document.createElement('DIV');
            date.align = 'right';
            var display = document.createElement('DIV');
            display.setAttribute('class', 'cal-display');
            if (indexDate.getFullYear() == TODAY.getFullYear() 
                && indexDate.getMonth() == TODAY.getMonth()
                && indexDate.getDate() == TODAY.getDate()) {
                cell.setAttribute('class', 'cal-today');
                date.setAttribute('class', 'cal-todate');
            } else if (indexDate.getMonth() == MONTH) {
                cell.setAttribute('class', 'cal-day');
                date.setAttribute('class', 'cal-date');
            } else {
                cell.setAttribute('class', 'cal-notmonth')
                date.setAttribute('class', 'cal-notmonth');
            }
            if (indexDate.getMonth() == MONTH && indexDate.getDate() in date_info) {
                display.innerHTML = date_info[indexDate.getDate()];
            }
            date.innerHTML = indexDate.getDate();
            cell.appendChild(date);
            cell.appendChild(display);
            indexDate.setDate(indexDate.getDate() + 1);
        }
    }
    div.appendChild(headerTable);
    div.appendChild(table);
}

renderCalendar(DIV);
