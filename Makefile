# Run cargo raze on the rust dependencies
raze:
	cd third_party/cargo; \
	cargo raze; \
	mv BUILD BUILD.suffix; \
	cat BUILD.prefix BUILD.suffix > BUILD; \
	rm BUILD.suffix; \
	sed -i 's#":protobuf_build_script",#":protobuf_build_script","@dayfine_xlab//third_party/cargo:rustc",#' remote/protobuf-*.BUILD; \
