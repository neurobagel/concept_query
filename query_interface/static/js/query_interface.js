// Author: Jonathan Armoza
// Created: November 4, 2021
// Purpose: JS for the query demo

class QueryPrototypeResultsHandler {

    static data_list = [];

    constructor(p_queryID) {

        // 1. Define instance fields
        this.queryID = parseInt(p_queryID);

        // 2. Initialize class instance
        this.setup();
        this.addEventListeners();
    }

    addEventListeners() {

        // 1. Add event listeners

        // A. Check all checkbox
        $("#dataset-checkall").click(function () {

            // I. Check or uncheck all
            $(".dataset-checkbox").prop("checked", $(this).prop("checked"));

            // II. Add all or remove all datasets from list
            if ( $(this).prop("checked") ) {

                // a. Add each corresponding dataset ID to the data list
                $(".dataset-checkbox").each(function(i, obj) {
                    QueryPrototypeResultsHandler.data_list.push($(this).attr("id"));
                });

                // b. Make the download results button visible
                $("#download-results-button").prop("disabled", false);
            }
            else {

                // a. Clear the data list
                QueryPrototypeResultsHandler.data_list = [];

                // b. Hide the download results button
                $("#download-results-button").prop("disabled", true);
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

        // 1. Define individual checkbox clicking behavior (not check all checkbox)
        $(".dataset-checkbox").not("#dataset-checkall").click(function() {
            
            // A. If checked, add the dataset id to the data list
            if ( $(this).prop("checked") ) {
                
                // a. Add this dataset's ID to the data list
                QueryPrototypeResultsHandler.data_list.push($(this).attr("id"));

                // b. Make the download results button visible
                $("#download-results-button").prop("disabled", false);
            } 
            // B. Otherwise, remove the dataset id from the data list
            else {
                
                // a. Remove this dataset's ID from the data list
                let index = QueryPrototypeResultsHandler.data_list.indexOf($(this).attr("id"));
                if ( index > -1 ) {
                    QueryPrototypeResultsHandler.data_list.splice(index, 1);
                }

                // b. Hide the download results button
                if ( 0 == QueryPrototypeResultsHandler.data_list.length ) {
                    
                    $("#download-results-button").prop("disabled", true);
                }
            }
        });
    }

    downloadCsv() {

        var data_json = {
            
            "query": this.queryID,
            "datasets": QueryPrototypeResultsHandler.data_list
        }
        this.sendPostWithData(`${location.origin}/query_interface/download_csv/`, JSON.stringify(data_json), "text/csv");
    }

    sendPostWithData(p_url, p_data, p_contentType) {

        $(document).ready(function() {
            
            $.ajax({

                method: "POST",
                url: p_url,
                data: p_data,
                success: function(blob, status, xhr) {
                    
                    // 1. Check for a filename
                    var filename = "";
                    var disposition = xhr.getResponseHeader('Content-Disposition');

                    if ( disposition && disposition.indexOf('attachment' ) !== -1 ) {
                        
                        var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        var matches = filenameRegex.exec(disposition);
                        
                        if ( matches != null && matches[1] ) {
                            filename = matches[1].replace(/['"]/g, '');
                        }
                    }
            
                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                        window.navigator.msSaveBlob(blob, filename);
                    } else {

                        var URL = window.URL || window.webkitURL;
                        var fileObj = new File([blob], filename, {type: p_contentType})
                        var downloadUrl = URL.createObjectURL(fileObj);
            
                        if ( filename ) {

                            // Use HTML5 a[download] attribute to specify filename
                            var a = document.createElement("a");

                            // Safari doesn't support this yet
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



