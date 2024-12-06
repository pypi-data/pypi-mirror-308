// code generated with the lngen, please not edit this file.
use std::io::{Read, Write};

use fundamentals_derive::{DecodeWire, EncodeWire};
#[cfg(feature = "pyo3")]
use pyo3::prelude::*;

use crate::core::{FromWire, ToWire};
use crate::prelude::*;

#[cfg_attr(feature = "pyo3", pyclass(set_all))]
#[derive(DecodeWire, EncodeWire, Debug, Clone)]
pub struct Error {
    #[msg_type = 17]
    pub ty: u16,
    pub channel_id: ChannelId,
    pub data: BitFlag,
}

#[cfg_attr(feature = "pyo3", pyclass(set_all))]
#[derive(DecodeWire, EncodeWire, Debug, Clone)]
pub struct Init {
    #[msg_type = 16]
    pub ty: u16,
    pub globalfeatures: BitFlag,
    pub features: BitFlag,
    pub init_tlvs: Stream,
}

/// Python impl method to expose python API
#[cfg_attr(feature = "pyo3", pymethods)]
impl Init {
    #[new]
    fn new() -> PyResult<Self> {
        Ok(Self {
            ty: 16,
            globalfeatures: BitFlag::default(),
            features: BitFlag::default(),
            init_tlvs: Stream::default(),
        })
    }
}

#[cfg_attr(feature = "pyo3", pyclass(set_all))]
#[derive(DecodeWire, EncodeWire, Debug, Clone)]
pub struct Ping {
    #[msg_type = 18]
    pub ty: u16,
    pub num_pong_bytes: u16,
    pub ignored: BitFlag,
}

#[cfg_attr(feature = "pyo3", pyclass(set_all))]
#[derive(DecodeWire, EncodeWire, Debug, Clone)]
pub struct Pong {
    #[msg_type = 19]
    pub ty: u16,
    pub ignored: BitFlag,
}

#[cfg_attr(feature = "pyo3", pyclass(set_all))]
#[derive(DecodeWire, EncodeWire, Debug, Clone)]
pub struct Warning {
    #[msg_type = 1]
    pub ty: u16,
    pub channel_id: ChannelId,
    pub data: BitFlag,
}
