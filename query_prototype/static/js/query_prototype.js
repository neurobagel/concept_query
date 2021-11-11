// Author: Jonathan Armoza
// Created: November 4, 2021
// Purpose: JS for the query demo

class QueryPrototypeResultsHandler {

    // static id_downloadResults = "#download-results";
    // static id_resultsCheckAll = "#dataset-checkall";
    // static class_resultsCheckbox = ".dataset-checkbox";

    constructor(p_queryID) {

        // 1. Define instance fields
        this.data_list = [];
        this.data_json = {

            "query": parseInt(p_queryID),
            "datasets": this.data_list
        };

        // 2. Initialize class instance
        this.setup();
        this.addEventListeners();
    }

    addEventListeners() {

        // 1. Save reference to this.data_list for use in event listeners
        let data_list = this.data_list;

        // 2. Add event listeners

        // A. Check all checkbox
        $("#dataset-checkall").click(function () {

            // I. Check or uncheck all
            $(".dataset-checkbox").prop("checked", $(this).prop("checked"));

            // II. Add all or remove all datasets from list
            if ( $(this).prop("checked") ) {

                // a. Add each corresponding dataset ID to the data list
                $(".dataset-checkbox").each(function(i, obj) {
                    data_list.push($(this).attr("id"));
                });

                // b. Make the download results button visible
                $("#download-results-button").css("visibility", "visible");
            }
            else {

                // a. Clear the data list
                data_list = [];

                // b. Hide the download results button
                $("#download-results-button").css("visibility", "hidden");
            }
        });

        // B. Download results button
        $("#download-results-button").click(function(){
            this.downloadCsv();
        }.bind(this));
        
        // C. All other checkboxes next to results
        this.addEventListenersCheckboxes();
    }

    addEventListenersCheckboxes(){

        // 1. Save reference to this.data_list for use in event listeners
        let data_list = this.data_list;

        // 2. Define individual checkbox clicking behavior (not check all checkbox)
        $(".dataset-checkbox").not("#dataset-checkall").click(function() {
            
            // A. If checked, add the dataset id to the data list
            if ( $(this).prop("checked") ) {
                
                // a. Add this dataset's ID to the data list
                data_list.push($(this).attr("id"));

                // b. Make the download results button visible
                $("#download-results-button").css("visibility", "visible");
            } 
            // B. Otherwise, remove the dataset id from the data list
            else {
                
                // a. Remove this dataset's ID from the data list
                let index = data_list.indexOf($(this).attr("id"));
                if ( -1 == index ) {
                    data_list.splice(index, 1);
                }

                // b. Hide the download results button
                $("#download-results-button").css("visibility", "hidden");
            }
        });

    }

    downloadCsv() {

        this.sendPostWithData(`${location.origin}/query_prototype/download_csv/`, JSON.stringify(this.data_json), "text/csv");
        // window.location = `${location.origin}/query_prototype/download_csv/`;
    }

    sendPostWithData(p_url, p_data, p_contentType) {

        $(document).ready(function() {
            
            $.ajax({

                method: "POST",
                url: p_url,
                data: p_data,
                // success: function (data) {
                //     //this gets called when server returns an OK response
                //     alert("it worked!");
                // },
                // error: function (data) {
                //     alert("it didnt work");
                // }
                success: function(blob, status, xhr) {
                    // check for a filename
                    var filename = "";
                    var disposition = xhr.getResponseHeader('Content-Disposition');
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        var matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                    }
            
                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                        window.navigator.msSaveBlob(blob, filename);
                    } else {
                        var URL = window.URL || window.webkitURL;
                        // var actualBlob = new Blob(blob);
                        var fileObj = new File([blob], filename, {type: p_contentType})
                        var downloadUrl = URL.createObjectURL(fileObj);
            
                        if (filename) {
                            // use HTML5 a[download] attribute to specify filename
                            var a = document.createElement("a");
                            // safari doesn't support this yet
                            if (typeof a.download === 'undefined') {
                                window.location.href = downloadUrl;
                            } else {
                                a.href = downloadUrl;
                                a.download = filename;
                                document.body.appendChild(a);
                                a.click();
                            }
                        } else {
                            window.location.href = downloadUrl;
                        }
            
                        setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                    }
                }                
            });
        });
    }

    setup() {

        // Adds CSRF token to headers of AJAX POST requests
        // See: https://www.skillsugar.com/how-to-add-django-csrf-token-to-jquery-ajax-function
        $(function() {

            $.ajaxSetup({
                headers: {
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val()
                }
            })
        });
    }
}



