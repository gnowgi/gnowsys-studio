;; This file is part of Ymacs for GNOWSYS: Gnowledge Networking 
;; and Organizing System.

;; Ymacs is free software; you can redistribute it and/or modify
;; it under the terms of the GNU Affero General Public License as
;; published by the Free Software Foundation; either version 3 of
;; the License, or (at your option) any later version.

;; Ymacs is distributed in the hope that it will be useful, but
;; WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU Affero General Public
;; License along with Ymacs (agpl.txt); if not, write to the
;; Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
;; Boston, MA  02110-1301  USA59 Temple Place, Suite 330,

;; Author: Divya <divyas15@gmail.com>


(defcustom gnow-server-port 9292
  "Local port the gnow server listens to."
  :group 'gnow-server
  :type 'integer)

(defcustom gnow-server-host nil
  "If not nil, accept connections from HOST address rather than just
localhost. This may present a security issue."
  :group 'gnow-server
  :type 'boolean)

(defcustom gnow-server-verbose nil
  "If not nil, log connections and progress also to the echo area."
  :group 'gnow-server
  :type 'boolean)

(defcustom gnow-server-done-hook nil
  "Hook run when done gnowing a buffer for the Emacs HTTP gnow-server.
Current buffer holds the text that is about to be sent back to the client."
  :group 'gnow-server
  :type 'hook)

; frame options
(defcustom gnow-server-new-frame t
  "If not nil, gnow each buffer in a new frame (and raise it)."
  :group 'gnow-server
  :type 'boolean)

(defcustom gnow-server-new-frame-minibuffer t
  "Show the emacs frame's minibuffer if set to t; hide if nil."
  :group 'gnow-server
  :type 'boolean)

(defcustom gnow-server-new-frame-menu-bar t
  "Show the emacs frame's menu-bar if set to t; hide if nil."
  :group 'gnow-server
  :type 'boolean)

(defcustom gnow-server-new-frame-mode-line t
  "Show the emacs frame's mode-line if set to t; hide if nil."
  :group 'gnow-server
  :type 'boolean)

;; Vars
(defconst gnow-server-process-buffer-name " *gnow-server*"
  "Template name of the gnow-server process buffers.")

(defconst gnow-server-log-buffer-name "*gnow-server-log*"
  "Template name of the gnow-server process buffers.")

(defconst gnow-server-gnow-buffer-name "TEXTAREA"
  "Template name of the gnow-server text editing buffers.")

(defconst gnow-server-new-frame-title "Emacs TEXTAREA"
  "Template name of the emacs frame's title.")

(defconst gnow-server-new-frame-width 80
  "The emacs frame's width.")

(defconst gnow-server-new-frame-height 25
  "The emacs frame's height.")

(defvar gnow-server-proc 'nil
  "Network process associated with the current edit, made local when
 the edit buffer is created")

(defvar gnow-server-frame 'nil
  "The frame created for a new gnow-server process, made local when
 then gnow buffer is created")

(defvar gnow-server-clients '() 
  "List of all client processes associated with the server process.")

(defvar gnow-server-phase nil 
  "Symbol indicating the state of the HTTP request parsing.")

(defvar gnow-server-received nil 
  "Number of bytes received so far in the client buffer. 
Depending on the character encoding, may be different from the buffer length.")

(defvar gnow-server-request nil 
  "The HTTP request (GET, HEAD, POST) received.")

(defvar gnow-server-content-length nil 
  "The value gotten from the HTTP `Content-Length' header.")

(defvar gnow-server-url nil 
  "The value gotten from the HTTP `x-url' header.")


;; Gnow Server socket code
;

(defun gnow-server-start (&optional verbose) 
  "Start the gnow server.

If argument VERBOSE is non-nil, logs all server activity to buffer `*gnow-server-log*'.
When called interactivity, a prefix argument will cause it to be verbose.
"
  (interactive "P")
  (if (process-status "gnow-server")
      (message "An gnow-server process is already running")
    (make-network-process
     :name "gnow-server"
     :buffer gnow-server-process-buffer-name
     :family 'ipv4
     :host (if gnow-server-host
	       gnow-server-host
	     'local)
     :service gnow-server-port
     :log 'gnow-server-accept
     :server 't)
    (setq gnow-server-clients '())
    (if verbose (get-buffer-create gnow-server-log-buffer-name))
    (gnow-server-log nil "Created a new gnow-server process")))

(defun gnow-server-stop nil
  "Stop the gnow server"
  (interactive)
  (while gnow-server-clients
    (gnow-server-kill-client (car gnow-server-clients))
    (setq gnow-server-clients (cdr gnow-server-clients)))
  (if (process-status "gnow-server")
      (delete-process "gnow-server")
    (message "No gnow server running"))
  (if (get-buffer gnow-server-process-buffer-name)
      (kill-buffer gnow-server-process-buffer-name)))

(defun gnow-server-log (proc fmt &rest args)
  "If a `*gnow-server-log*' buffer exists, write STRING to it for logging purposes.
If `gnow-server-verbose' is non-nil, then STRING is also echoed to the message line."
  (let ((string (apply 'format fmt args)))
    (if gnow-server-verbose
        (message string))
    (if (get-buffer gnow-server-log-buffer-name)
        (with-current-buffer gnow-server-log-buffer-name
          (goto-char (point-max))
          (insert (current-time-string) 
                  " " 
                  (if (processp proc)
                      (concat 
                       (buffer-name (process-buffer proc))
                       ": ")
                    "") ; nil is not acceptable to 'insert
                  string)
          (or (bolp) (newline))))))

(defun gnow-server-accept (server client msg)
  "Accept a new client connection."
  (let ((buffer (generate-new-buffer gnow-server-process-buffer-name)))
    (buffer-disable-undo buffer)
    (set-process-buffer client buffer)
    (set-process-filter client 'gnow-server-filter)
    (set-process-query-on-exit-flag client nil) ; kill-buffer kills the associated process
    (with-current-buffer buffer
      (set (make-local-variable 'gnow-server-phase) 'wait)
      (set (make-local-variable 'gnow-server-received) 0)
      (set (make-local-variable 'gnow-server-request) nil))
      (set (make-local-variable 'gnow-server-content-length) nil)
      (set (make-local-variable 'gnow-server-url) nil))
    (add-to-list 'gnow-server-clients client)
    (gnow-server-log client msg))

(defun gnow-server-filter (proc string)
  "Process data received from the client."
  ;; there is no guarantee that data belonging to the same client
  ;; request will arrive all in one go; therefore, we must accumulate
  ;; data in the buffer and process it in different phases, which
  ;; requires us to keep track of the processing state.
  (with-current-buffer (process-buffer proc)
    (insert string)
    (setq gnow-server-received 
          (+ gnow-server-received (string-bytes string)))
    (when (eq gnow-server-phase 'wait)
      ;; look for a complete HTTP request string
      (save-excursion
        (goto-char (point-min))
        (when (re-search-forward "^\\([A-Z]+\\)\\s-+\\(\\S-+\\)\\s-+\\(HTTP/[0-9\.]+\\)\r?\n" nil t)
          (gnow-server-log proc 
                           "Got HTTP `%s' request, processing in buffer `%s'..." 
                           (match-string 1) (current-buffer))
          (setq gnow-server-request (match-string 1))
          (setq gnow-server-content-length nil)
          (setq gnow-server-phase 'head))))
    
    (when (eq gnow-server-phase 'head)
      ;; look for "Content-length" header
      (save-excursion
        (goto-char (point-min))
        (when (re-search-forward "^Content-Length:\\s-+\\([0-9]+\\)" nil t)
          (setq gnow-server-content-length (string-to-number (match-string 1)))))
      (save-excursion
        (goto-char (point-min))
        (when (re-search-forward "\\(\r?\n\\)\\{2\\}" nil t)
          ;; HTTP headers are pure ASCII (1 char = 1 byte), so we can subtract
          ;; the buffer position from the count of received bytes
          (setq gnow-server-received
                (- gnow-server-received (- (match-end 0) (point-min))))
          ;; discard headers - keep only HTTP content in buffer
          (delete-region (point-min) (match-end 0))
          (setq gnow-server-phase 'body))))
    
    (when (eq gnow-server-phase 'body)
      (if (and gnow-server-content-length
               (> gnow-server-content-length gnow-server-received))
          (gnow-server-log proc 
                           "Received %d bytes of %d ..." 
                           gnow-server-received gnow-server-content-length)
        ;; all content transferred - process request now
        (cond
         ((string= gnow-server-request "POST")
          ;; create gnowing buffer, and move content to it
          (gnow-server-create-gnow-buffer proc)
	  )
         (t
          ;; send 200 OK response to any other request
          (gnow-server-send-response proc "gnow-server is running.\n" t)))
        ;; wait for another connection to arrive
        (setq gnow-server-received 0)
        (setq gnow-server-phase 'wait)))))


(defun gnow-server-create-gnow-buffer(proc)
  "Create an gnow buffer, place content in it and save the network
  process for the final call back"

  (let ((buffer (generate-new-buffer gnow-server-gnow-buffer-name)))
    (copy-to-buffer buffer (point-min) (point-max))
    (with-current-buffer (process-buffer proc)

      (save-excursion
        (goto-char (point-min))
        (when (re-search-forward "^gnow-select:\\s-+\\([a-zA-Z]+\\)" nil t)
          (setq gnow-server-url (match-string 1))
	  (delete-region (point-min) (match-end 0))
	  ))
     
      (setq buffer-file-name (concat (expand-file-name "~") "/gnowmacs.org"))
      (cond ((equal gnow-server-url "HTML")
	     (org-mode)
	     (org-export-as-html 3))
	    ((equal gnow-server-url "PDF")
	     (org-mode)
	     (org-export-as-pdf 3))
	    ((equal gnow-server-url "LaTeX")
	     (org-mode)
	     (org-export-as-latex 3))
	    ((equal gnow-server-url "DocBook")
	     (org-mode)
	     (org-export-as-docbook))
	    ((equal gnow-server-url "XOXO")
	     (org-mode)
	     (org-export-as-xoxo))
	    )
	    
      )))


(defun gnow-server-send-response (proc &optional body close)
  "Send an HTTP 200 OK response back to process PROC.
Optional second argument BODY specifies the response content:
  - If nil, the HTTP response will have null content.
  - If a string, the string is sent as response content.
  - Any other value will cause the contents of the current 
    buffer to be sent.
If optional third argument CLOSE is non-nil, then process PROC
and its buffer are killed with `gnow-server-kill-client'."
  (interactive)
rqxbk  (if (processp proc)
      (let ((response-header (concat
                          "HTTP/1.0 200 OK\n"
                          (format "Server: Emacs/%s\n" emacs-version)
                          "Date: "
                          (format-time-string
                           "%a, %d %b %Y %H:%M:%S GMT\n"
                           (current-time)))))
        (process-send-string proc response-header)
        (process-send-string proc "\n")
        (cond
         ((stringp body) (process-send-string proc body))
         ((not body) nil)
         (t (process-send-region proc (point-min) (point-max))))
        (process-send-eof proc)
        (if close 
            (gnow-server-kill-client proc))
        (gnow-server-log proc "Gnowing done, sent HTTP OK response."))
    (message "gnow-server-send-response: invalid proc (bug?)")))

(defun gnow-server-kill-client (proc)
  "Kill client process PROC and remove it from the list."
  (let ((procbuf (process-buffer proc)))
    (delete-process proc)
    (kill-buffer procbuf)
    (setq gnow-server-clients (delq proc gnow-server-clients))))

(defun gnow-server-done (&optional abort nokill)
  "Finish gnowing: send HTTP response back, close client and gnowing buffers.

The current contents of the buffer are sent back to the HTTP
client, unless argument ABORT is non-nil, in which case then the
original text is sent back.
If optional second argument NOKILL is non-nil, then the gnowing
buffer is not killed.

When called interactively, use prefix arg to abort gnowing."
  (interactive "P")
  ;; Do nothing if the connection is closed by the browser (tab killed, etc.)
  (unless (eq (process-status gnow-server-proc) 'closed)
    (let ((buffer (current-buffer))
           (proc gnow-server-proc)
           (procbuf (process-buffer gnow-server-proc)))
      ;; gnow-server-* vars are buffer-local, so they must be used before issuing kill-buffer
      (if abort
        ;; send back original content
        (with-current-buffer procbuf
          (run-hooks 'gnow-server-done-hook)
          (gnow-server-send-response proc t))
        ;; send back gnowed content
        (save-restriction
          (widen)
          (buffer-disable-undo)
          ;; ensure any format encoding is done (like longlines)
          (dolist (format buffer-file-format)
            (format-encode-region (point-min) (point-max) format))
          ;; send back
          (run-hooks 'gnow-server-done-hook)
          (gnow-server-send-response gnow-server-proc t)
          ;; restore formats (only useful if we keep the buffer)
          (dolist (format buffer-file-format)
            (format-decode-region (point-min) (point-max) format))
          (buffer-enable-undo)))
      (if gnow-server-frame (delete-frame gnow-server-frame))
      ;; delete-frame may change the current buffer
      (unless nokill (kill-buffer buffer))
      (gnow-server-kill-client proc))))


(provide 'gnow-server)


