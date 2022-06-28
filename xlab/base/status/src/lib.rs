// Port https://github.com/abseil/abseil-cpp/blob/master/absl/status/status.h.

#[derive(Debug, PartialEq)]
pub enum StatusCode {
    // Ok is eliminated as it's not used.
    Cancelled = 1,
    Unknown = 2,
    InvalidArgument = 3,
    DeadlineExceeded = 4,
    NotFound = 5,
    AlreadyExists = 6,
    PermissionDenied = 7,
    Unauthenticated = 16,
    ResourceExhausted = 8,
    FailedPrecondition = 9,
    Aborted = 10,
    OutOfRange = 11,
    Unimplemented = 12,
    Internal = 13,
    Unavailable = 14,
    DataLoss = 15,
}

#[derive(Debug)]
pub struct Status {
    pub status_code: StatusCode,
    pub message: String,
}

impl StatusCode {
    fn as_str(&self) -> &'static str {
        match self {
            StatusCode::Cancelled => "Cancelled",
            StatusCode::Unknown => "Unknown",
            StatusCode::InvalidArgument => "InvalidArgument",
            StatusCode::DeadlineExceeded => "DeadlineExceeded",
            StatusCode::NotFound => "NotFound",
            StatusCode::AlreadyExists => "AlreadyExists",
            StatusCode::PermissionDenied => "PermissionDenied",
            StatusCode::Unauthenticated => "Unauthenticated ",
            StatusCode::ResourceExhausted => "ResourceExhausted",
            StatusCode::FailedPrecondition => "FailedPrecondition",
            StatusCode::Aborted => "Aborted ",
            StatusCode::OutOfRange => "OutOfRange ",
            StatusCode::Unimplemented => "Unimplemented ",
            StatusCode::Internal => "Internal ",
            StatusCode::Unavailable => "Unavailable ",
            StatusCode::DataLoss => "DataLoss ",
        }
    }
}

impl std::error::Error for Status {}

impl std::fmt::Display for Status {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}: {}",
            self.status_code.as_str().to_string(),
            self.message
        )
    }
}

fn make_status(status_code: StatusCode, message: &str) -> Status {
    Status {
        status_code,
        message: message.to_string(),
    }
}

pub fn cancelled_error(message: &str) -> Status {
    make_status(StatusCode::Cancelled, message)
}

pub fn unknown_error(message: &str) -> Status {
    make_status(StatusCode::Unknown, message)
}

pub fn invalid_argument_error(message: &str) -> Status {
    make_status(StatusCode::InvalidArgument, message)
}

pub fn deadline_exceeded_error(message: &str) -> Status {
    make_status(StatusCode::DeadlineExceeded, message)
}

pub fn not_found_error(message: &str) -> Status {
    make_status(StatusCode::NotFound, message)
}

pub fn already_exists_error(message: &str) -> Status {
    make_status(StatusCode::AlreadyExists, message)
}

pub fn permission_denied_error(message: &str) -> Status {
    make_status(StatusCode::PermissionDenied, message)
}

pub fn unauthenticated_error(message: &str) -> Status {
    make_status(StatusCode::Unauthenticated, message)
}

pub fn resource_exhausted_error(message: &str) -> Status {
    make_status(StatusCode::ResourceExhausted, message)
}

pub fn failed_precondition_error(message: &str) -> Status {
    make_status(StatusCode::FailedPrecondition, message)
}

pub fn aborted_error(message: &str) -> Status {
    make_status(StatusCode::Aborted, message)
}

pub fn out_of_range_error(message: &str) -> Status {
    make_status(StatusCode::OutOfRange, message)
}

pub fn unimplemented_error(message: &str) -> Status {
    make_status(StatusCode::Unimplemented, message)
}

pub fn internal_error(message: &str) -> Status {
    make_status(StatusCode::Internal, message)
}

pub fn unavailable_error(message: &str) -> Status {
    make_status(StatusCode::Unavailable, message)
}

pub fn data_loss_error(message: &str) -> Status {
    make_status(StatusCode::DataLoss, message)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cancelled_error_has_the_correct_code() {
        let e = cancelled_error("");
        assert_eq!(e.status_code, StatusCode::Cancelled);
    }

    #[test]
    fn unknown_error_has_the_correct_code() {
        let e = unknown_error("");
        assert_eq!(e.status_code, StatusCode::Unknown);
    }

    #[test]
    fn invalid_argument_error_has_the_correct_code() {
        let e = invalid_argument_error("");
        assert_eq!(e.status_code, StatusCode::InvalidArgument);
    }

    #[test]
    fn deadline_exceeded_error_has_the_correct_code() {
        let e = deadline_exceeded_error("");
        assert_eq!(e.status_code, StatusCode::DeadlineExceeded);
    }

    #[test]
    fn not_found_error_has_the_correct_code() {
        let e = not_found_error("");
        assert_eq!(e.status_code, StatusCode::NotFound);
    }

    #[test]
    fn already_exists_error_has_the_correct_code() {
        let e = already_exists_error("");
        assert_eq!(e.status_code, StatusCode::AlreadyExists);
    }

    #[test]
    fn permission_denied_error_has_the_correct_code() {
        let e = permission_denied_error("");
        assert_eq!(e.status_code, StatusCode::PermissionDenied);
    }

    #[test]
    fn unauthenticated_error_has_the_correct_code() {
        let e = unauthenticated_error("");
        assert_eq!(e.status_code, StatusCode::Unauthenticated);
    }

    #[test]
    fn resource_exhausted_error_has_the_correct_code() {
        let e = resource_exhausted_error("");
        assert_eq!(e.status_code, StatusCode::ResourceExhausted);
    }

    #[test]
    fn failed_precondition_error_has_the_correct_code() {
        let e = failed_precondition_error("");
        assert_eq!(e.status_code, StatusCode::FailedPrecondition);
    }

    #[test]
    fn aborted_error_has_the_correct_code() {
        let e = aborted_error("");
        assert_eq!(e.status_code, StatusCode::Aborted);
    }

    #[test]
    fn out_of_range_error_has_the_correct_code() {
        let e = out_of_range_error("");
        assert_eq!(e.status_code, StatusCode::OutOfRange);
    }

    #[test]
    fn unimplemented_error_has_the_correct_code() {
        let e = unimplemented_error("");
        assert_eq!(e.status_code, StatusCode::Unimplemented);
    }

    #[test]
    fn internal_error_has_the_correct_code() {
        let e = internal_error("");
        assert_eq!(e.status_code, StatusCode::Internal);
    }

    #[test]
    fn unavailable_error_has_the_correct_code() {
        let e = unavailable_error("");
        assert_eq!(e.status_code, StatusCode::Unavailable);
    }

    #[test]
    fn data_loss_error_has_the_correct_code() {
        let e = data_loss_error("");
        assert_eq!(e.status_code, StatusCode::DataLoss);
    }
}
